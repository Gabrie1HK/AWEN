from fastapi import HTTPException, status


class AppError(HTTPException):
    def __init__(self, status_code: int, message: str, detail: dict | None = None) -> None:
        payload = {"message": message}
        if detail:
            payload["detail"] = detail
        super().__init__(status_code=status_code, detail=payload)


class NotFoundError(AppError):
    def __init__(self, message: str, detail: dict | None = None) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, message, detail)


class UnauthorizedError(AppError):
    def __init__(self, message: str, detail: dict | None = None) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, message, detail)


class ForbiddenError(AppError):
    def __init__(self, message: str, detail: dict | None = None) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, message, detail)
