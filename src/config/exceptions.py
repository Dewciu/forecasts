class InitArgsCountError(Exception):
    """Exception raised, when invalid count of init args were parsed.

    Attrs:
        args - input args, which caused the error,
        message - explenation of the error
    """

    def __init__(self, args: list, message="Invalid count of initialization arguments."):
        self.args = args
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}: Should be 3 (input path, output path and mode)."

class InitArgsPathNotExists(Exception):
    """Exception raised, when invalid path from init args was parsed.

    Attrs:
        path - input path, which caused the error,
        message - explenation of the error
    """
    def __init__(self, path: str, message="Path does not exist"):
        self.path = path
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}: {self.path}"


class InitArgsInvalidModeType(Exception):
    """Exception raised, when invalid mode type from init args was parsed.

    Attrs:
        mode - input mode, which caused the error,
        message - explenation of the error
    """
    def __init__(self, mode: str, valid_modes: str, message="Invalid mode type"):
        self.mode = mode
        self.valid_modes = valid_modes
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}: {self.mode}. Valid mode types: {self.valid_modes}"