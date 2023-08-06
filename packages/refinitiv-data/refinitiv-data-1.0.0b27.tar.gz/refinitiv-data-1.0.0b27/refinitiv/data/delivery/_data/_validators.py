import abc
from typing import Iterable, List

from ._parsed_data import ParsedData


class BaseValidator(abc.ABC):
    @abc.abstractmethod
    def validate(self, data: ParsedData) -> bool:
        # for override
        pass


class ContentValidator(BaseValidator):
    def validate(self, data: ParsedData) -> bool:
        is_valid = True
        content_data = data.content_data

        if content_data is None:
            is_valid = False
            data.error_codes = 1
            data.error_messages = "Content data is None"

        else:
            status = content_data.get("status")
            if status == "Error":
                is_valid = False
                data.error_codes = content_data.get("code", -1)
                data.error_messages = content_data.get("message")

        return is_valid


class ContentTypeValidator(BaseValidator):
    def __init__(self, allowed_content_types=None):
        if allowed_content_types is None:
            allowed_content_types = {"application/json"}
        self._allowed_content_types = allowed_content_types

    def validate(self, data: ParsedData) -> bool:
        # Checking only first part (type/subtype) of media_type
        # See https://httpwg.org/specs/rfc7231.html#media.type
        content_type = (
            data.raw_response.headers.get("content-type", "").split(";")[0].strip()
        )
        is_success = content_type in self._allowed_content_types

        if not is_success:
            data.error_codes = -1
            data.error_messages = (
                f"Unexpected content-type in response,\n"
                f"Expected: {self._allowed_content_types}\n"
                f"Actual: {content_type}"
            )

        return is_success


class ValidatorContainer:
    def __init__(
        self,
        validators: Iterable = None,
        content_validator=ContentValidator(),
        content_type_validator=ContentTypeValidator(),
        use_default_validators=True,
    ):
        self.validators: List[BaseValidator] = list(validators) if validators else []
        if content_type_validator and use_default_validators:
            self.validators.append(content_type_validator)
        if content_validator and use_default_validators:
            self.validators.append(content_validator)

    def validate(self, data: ParsedData) -> bool:
        return all(validator.validate(data) for validator in self.validators)
