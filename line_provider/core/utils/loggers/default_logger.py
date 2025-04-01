import logging

from core.utils.loggers.base_logger import BaseLogger


class DefaultLogger(BaseLogger):
    def __init__(self, name: str | None = None) -> None:
        self._logger = logging.getLogger(name)

    @staticmethod
    def _create_details(message: str) -> dict:
        details = {
            "message": message,
        }
        return details

    def info(self, message: str) -> None:
        self._logger.info(self._create_details(message))

    def debug(self, message: str) -> None:
        self._logger.debug(self._create_details(message))

    def warning(self, message: str) -> None:
        self._logger.warning(self._create_details(message))

    def error(self, message: str) -> None:
        self._logger.error(self._create_details(message))

    def critical(self, message: str) -> None:
        self._logger.critical(self._create_details(message))

    def exception(self, message: str) -> None:
        self._logger.exception(self._create_details(message))
