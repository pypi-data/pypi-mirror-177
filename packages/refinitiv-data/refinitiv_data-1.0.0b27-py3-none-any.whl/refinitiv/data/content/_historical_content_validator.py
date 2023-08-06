import re
from typing import TYPE_CHECKING

from ..delivery._data._data_provider import ContentValidator

if TYPE_CHECKING:
    from ..delivery._data._data_provider import ParsedData

user_has_no_permissions_expr = re.compile(
    r"TS\.((Interday)|(Intraday))\.UserNotPermission\.[0-9]{5}"
)


class HistoricalContentValidator(ContentValidator):
    def validate(self, data: "ParsedData") -> bool:
        is_valid = True
        content_data = data.content_data

        if not content_data:
            is_valid = False

        elif isinstance(content_data, list) and len(content_data):
            content_data = content_data[0]
            status = content_data.get("status", {})
            code = status.get("code", "")

            if status and user_has_no_permissions_expr.match(code):
                is_valid = False
                data.status["error"] = status
                data.error_codes = code
                data.error_messages = status.get("message")

            elif "Error" in code:
                is_valid = False
                data.status["error"] = status
                data.error_codes = code
                data.error_messages = status.get("message")

                if not (content_data.keys() - {"universe", "status"}):
                    is_valid = False

                elif "UserRequestError" in code:
                    is_valid = True

        return is_valid
