from typing import TYPE_CHECKING

from ..delivery._data._data_provider import ContentValidator

if TYPE_CHECKING:
    from ..delivery._data._data_provider import ParsedData
    import httpx


def get_invalid_universes(universes):
    result = []
    for universe in universes:
        if universe.get("Organization PermID") == "Failed to resolve identifier(s).":
            result.append(universe.get("Instrument"))
    return result


def get_universe_from_raw_response(raw_response: "httpx.Response"):
    universe = raw_response.url.params["universe"]
    universe = universe.split(",")
    return universe


class UniverseContentValidator(ContentValidator):
    def validate(self, data: "ParsedData") -> bool:
        is_valid = super().validate(data)
        if not is_valid:
            return is_valid

        content_data = data.content_data
        error = content_data.get("error", {})
        universes = content_data.get("universe", [])
        invalid_universes = get_invalid_universes(universes)

        if error:
            is_valid = False
            data.error_codes = error.get("code")

            error_message = error.get("description")
            if error_message == "Unable to resolve all requested identifiers.":
                universe = get_universe_from_raw_response(data.raw_response)
                error_message = f"{error_message} Requested items: {universe}"

            if not error_message:
                error_message = error.get("message")
                errors = error.get("errors")
                if isinstance(errors, list):
                    errors = "\n".join(map(str, errors))
                    error_message = f"{error_message}:\n{errors}"
            data.error_messages = error_message

        elif invalid_universes:
            data.error_messages = f"Failed to resolve identifiers {invalid_universes}"

        return is_valid
