import os

from typing import Union
from datetime import datetime
from pathlib import Path, PurePath
from requests.packages import urllib3
from eagleRpaUtility.CentralizedLogger import CentralizedLogger, ResponseNot200, ServerConnectionError, UnknownError
from logging import Logger, StreamHandler, FileHandler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL

class CustomLogger(Logger):
    urllib3.disable_warnings()
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.central_logger: CentralizedLogger = CentralizedLogger()
        self.logger_setted_up: bool = False
        self.server_error: bool = True
        self.only_local: bool = False

    def setupLogger(self, log_path: str = None, console_level: int = DEBUG, file_level: int = DEBUG) -> None:
        self.setLevel(DEBUG)
        format_template = "%(asctime)s - %(levelname)s - %(message)s"
        if console_level is not None:
            c_handler = StreamHandler()
            c_handler.setLevel(console_level)
            c_format = Formatter(format_template, datefmt="%d-%m-%Y %H:%M:%S")
            c_handler.setFormatter(c_format)
            self.addHandler(c_handler)
        if log_path is not None:
            log_path = Path(log_path)
            if not log_path.is_dir():
                os.mkdir(log_path)
            creation_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            f_handler = FileHandler(PurePath(log_path, f"{creation_time}.log"))
            f_handler.setLevel(file_level)
            f_format = Formatter(format_template, datefmt="%d-%m-%Y %H:%M:%S")
            f_handler.setFormatter(f_format)
            self.addHandler(f_handler)
        self.logger_setted_up = True

    def setupCentralizedLogger(self, automation=None, client=None, developer=None) -> bool:
        if self.logger_setted_up:
            try:
                self.central_logger.setupRun(automation, client, developer)
            except ResponseNot200:
                self.server_error = True
                self.error("Error adding run to central logger! Central Logger disabled!")
            except ServerConnectionError:
                self.server_error = True
                self.error("Server error adding run to central logger! Central Logger disabled!")
            except UnknownError as e:
                self.server_error = True
                self.error("Unknown error adding run to central logger! Central Logger disabled!")
                print(e)
                self.info("UnknownError", e)
            self.only_local = False
            return True
        self.only_local = True
        self.server_error = True
        self.error("Error local logger not setted! Central Logger disabled!")
        return False

    def getRunId(self) -> Union[str, None]:
        return self.central_logger.id_run

    def setRunId(self, id: str) -> None:
        self.central_logger.id_run = id

    def checkAddLogRequest(self, message: str, level: int) -> None:
        if not (self.server_error or self.only_local):
            try:
                return self.central_logger.addLog(message, level)
            except ResponseNot200:
                self.error("Error adding log to central logger!")
            except ServerConnectionError:
                self.server_error = True
                self.error("Server error, failed adding log to central logger! Central Logger disabled!")
            except UnknownError as e:
                self.server_error = True
                self.error("Error adding log to central logger! Central Logger disabled!")
                self.exception("UnknownError", e)

    def debug(self, message: str, only_local: bool =False) -> None:
        super().debug(message)
        if not only_local:
            self.checkAddLogRequest(message, DEBUG)

    def info(self, message: str, only_local: bool =False) -> None:
        super().info(message)
        if not only_local:
            self.checkAddLogRequest(message, INFO)

    def warning(self, message: str, only_local: bool =False) -> None:
        super().warning(message)
        if not only_local:
            self.checkAddLogRequest(message, WARNING)

    def error(self, message: str, only_local: bool =False) -> None:
        super().error(message)
        if not only_local:
            self.checkAddLogRequest(message, ERROR)

    def exception(self, message: str, exc=None, only_local: bool=False) -> None:
        super().error(message, exc_info=True)
        if not only_local:
            self.checkAddLogRequest(message+str(exc), ERROR)

    def critical(self, message: str, only_local: bool =False) -> None:
        super().critical(message)
        if not only_local:
            self.checkAddLogRequest(message, CRITICAL)