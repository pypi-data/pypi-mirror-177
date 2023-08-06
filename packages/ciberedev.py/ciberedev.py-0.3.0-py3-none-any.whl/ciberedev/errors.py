class BaseError(Exception):
    pass


class ClientNotStarted(BaseError):
    def __init__(self):
        super().__init__(
            "Client has not been started. You can start it with 'client.run' or 'client.start'"
        )


class ClientAlreadyStarted(BaseError):
    def __init__(self):
        super().__init__("Client has already been started")


class UnknownError(BaseError):
    def __init__(self, error: str):
        self.error = error
        super().__init__(f"An unknown error has occured: {error}")


class AuthorizationError(BaseError):
    pass


class NoAuthorizationGiven(AuthorizationError):
    def __init__(self):
        super().__init__("No Authorization Passed When Creating Client Instance")


class InvalidAuthorizationGiven(AuthorizationError):
    def __init__(self):
        super().__init__("Invalid Authorization Given")


class EmbedError(BaseError):
    pass


class UnknownEmbedField(EmbedError):
    def __init__(self, field: str):
        self.field = field
        super().__init__(f"Unknown Embed Field Given: '{self.field}'")


class ScreenshotError(BaseError):
    pass


class InvalidURL(ScreenshotError):
    def __init__(self, url: str):
        self.url = url
        super().__init__(f"Invalid URL Given: '{self.url}'")


class UnableToConnect(ScreenshotError):
    def __init__(self, url: str):
        self.url = url
        super().__init__(f"Unable to Connect to '{self.url}'")


class FileUpoadError(BaseError):
    pass


class InvalidFilePath(FileUpoadError):
    def __init__(self, path: str):
        self.path = path
        super().__init__(f"Invalid File Path Given: '{path}'")


class UnknownMimeType(FileUpoadError):
    def __init__(self, ext: str):
        super().__init__(
            f"I could not find the mimetype for the file extention: '{ext}' please provide your own."
        )
        self.ext = ext
