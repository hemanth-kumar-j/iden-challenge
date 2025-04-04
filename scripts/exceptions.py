class PopupNotFoundError(Exception):
    """Custom exception for missing or invalid popup messages."""

    def __init__(self, message):
        super().__init__(message)
