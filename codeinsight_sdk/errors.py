class GenericError(Exception): #pragma: no cover
    """Generic error class, catch-all for most code insight API errors."""
    pass

class NotYetImplementedError(Exception): #pragma: no cover
    """Error class for API features that have not yet been implemented."""
    pass
