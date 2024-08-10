from fastapi import HTTPException


class ApplicationError(HTTPException):
    pass


class UserExistsError(ApplicationError):
    pass


class UserNotFoundError(ApplicationError):
    pass


class WeakPasswordError(ApplicationError):
    pass
