

class PatternError(Exception):
    pass


class CheckError(Exception):
    pass


class PatternFormatError(PatternError):
    pass


class ParameterFormatError(Exception):
    pass
