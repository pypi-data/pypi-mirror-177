class QmQuaException(Exception):
    pass


class OpenQmException(QmQuaException):
    pass


class FailedToExecuteJobException(QmQuaException):
    pass


class FailedToAddJobToQueueException(QmQuaException):
    pass


class CompilationException(QmQuaException):
    pass


class JobCancelledError(QmQuaException):
    pass


class InvalidStreamMetadataError(QmQuaException):
    pass


class ConfigValidationException(QmQuaException):
    pass


class ConfigSerializationException(QmQuaException):
    pass


class InvalidConfigError(QmQuaException):
    pass
