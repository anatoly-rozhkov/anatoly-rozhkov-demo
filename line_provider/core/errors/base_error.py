from starlette import status


class BaseError(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Internal Server Error"
    message: str = "Something went wrong"

    def __init__(
        self,
        status_code: int | None = None,
        detail: str | None = None,
        message: str | None = None,
    ) -> None:
        self.detail = detail or self.detail
        self.message = message or self.message
        self.status_code = status_code or self.status_code
