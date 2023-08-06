import abc
from typing import Tuple

from .._core.session import get_default
from .._errors import RDError
from .._fin_coder_layer import get_adc_data
from .._tools import cached_property
from ..content.pricing import chain
from ..content.pricing.chain._stream_facade import Stream

default_error_message = "No values to unpack"


class UniverseExpander:
    @property
    @abc.abstractmethod
    def _universe(self):
        pass

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self):
        if self._n < len(self._universe):
            result = self._universe[self._n]
            self._n += 1
            return result
        raise StopIteration


def update_universe(raw, _universe):
    index = 0  # instrument
    data = raw.get("data")
    if data and all(isinstance(i[index], str) for i in data):
        universe = [i[index] for i in data]
    else:
        universe = _universe
    return universe


def get_universe(expression):
    session = get_default()
    logger = session.logger()
    adc_raw, _ = get_adc_data(
        params={
            "universe": expression,
            "fields": "TR.RIC",
        },
        logger=logger,
        raise_if_error=True,
    )
    return update_universe(
        adc_raw,
        None,
    )


class DiscoveryUniverse(UniverseExpander):
    def __init__(self, expression):
        self._expression = expression

    @property
    def expression(self):
        return self._expression

    @cached_property
    def _universe(self):
        universe = get_universe(self._expression)
        if not universe:
            raise RDError(-1, default_error_message)
        return universe


class Peers(DiscoveryUniverse):
    """
    Class to get data from peers function.

    Parameters
    ----------
    expression : str
        peers expression


    Examples
    --------
    >>> peers = Peers("VOD.L")
    >>> print(list(peers))
    """

    def __init__(self, expression):
        super().__init__(f"peers({expression})")


class Screener(DiscoveryUniverse):
    """
    Class to get data from screen function.

    Parameters
    ----------
    expression : str
        screen expression


    Examples
    --------
    >>> screener = Screener('U(IN(Equity(active,public,primary))/*UNV:Public*/), IN(TR.HQCountryCode,"AR"), IN(TR.GICSIndustryCode,"401010")')
    >>> print(list(screener))
    """

    def __init__(self, expression):
        super().__init__(f"screen({expression})")


def on_error_callback(data: Tuple[dict], universe: str, stream: Stream):
    state = data[0].get("State", {})
    message = state.get("Text", default_error_message)
    code = state.get("Code", -1)
    stream.close()
    raise RDError(code, message)


class Chain(UniverseExpander):
    """
    Class to get data from chain.

    Parameters
    ----------
    name : str
        chain name


    Examples
    --------
    >>> chain = Chain("0#.DJI")
    >>> print(list(chain))
    >>> print(chain.constituents)
    >>> print(chain.summary_links)
    """

    def __init__(self, name):
        self._name = name

    @cached_property
    def _chains(self):
        chain_stream = chain.Definition(self._name).get_stream()
        chain_stream.on_complete(lambda *_: chain_stream.close())
        chain_stream.open()
        if not chain_stream.constituents:
            raise RDError(-1, default_error_message)
        return chain_stream

    @property
    def name(self):
        return self._name

    @property
    def summary_links(self):
        return self._chains.summary_links

    @property
    def constituents(self):
        return self._chains.constituents

    @property
    def _universe(self):
        return self.constituents
