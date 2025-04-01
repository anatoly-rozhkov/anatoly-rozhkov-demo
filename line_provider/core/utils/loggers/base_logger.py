from abc import ABC, abstractmethod
from typing import TypeVar


class BaseLogger(ABC):
    name: str | None

    @abstractmethod
    def info(self, message: str) -> None:
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def debug(self, message: str) -> None:
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def warning(self, message: str) -> None:
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def error(self, message: str) -> None:
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def critical(self, message: str) -> None:
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def exception(self, exc: str) -> None:
        raise NotImplementedError("Not implemented")


Logger = TypeVar("Logger", bound=BaseLogger)
