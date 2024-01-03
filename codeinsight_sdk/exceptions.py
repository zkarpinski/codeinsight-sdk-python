
import requests
import json

class GenericError(Exception): #pragma: no cover
    """Generic error class, catch-all for most code insight API errors."""
    pass

class NotYetImplementedError(Exception): #pragma: no cover
    """Error class for API features that have not yet been implemented."""
    pass

class CodeInsightError(GenericError):
    """Error class for code insight API errors."""
    def __init__(self, response: requests.Response):
        try:
            resp = response.json()
            self.code = response.status_code
            self.message = resp['Error: ']
            self.arguments = resp['Arguments: ']
            self.error = resp['Key: ']
            self.add_note(f"Arguments: {self.arguments}")
            super().__init__("Error: %s - %s" % (self.code, self.message))

        except KeyError:
            raise ValueError(f"Error parsing response: {resp}")
        except json.decoder.JSONDecodeError:
            raise ValueError(f"Error decoding response: {resp}")
