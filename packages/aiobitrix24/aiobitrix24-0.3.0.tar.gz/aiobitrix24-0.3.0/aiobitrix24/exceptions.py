class BadBitrixResponseError(Exception):
    """Bad response from bx24."""


class BatchError(Exception):
    """Rises if batch size is more than 50."""
