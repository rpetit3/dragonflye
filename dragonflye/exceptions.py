class DependencyError(Exception):
    pass

class MissingDependencyError(DependencyError):
    pass

class InvalidDependencyError(DependencyError):
    pass

class InvalidDependencyVersionError(DependencyError):
    pass

class MissingInputError(Exception):
    pass
