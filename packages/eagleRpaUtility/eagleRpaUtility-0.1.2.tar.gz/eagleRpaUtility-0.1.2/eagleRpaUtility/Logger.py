import os
import logging

from pathlib import Path, PurePath
from datetime import datetime


def setupLogging(log_path: str, console_level:int =logging.DEBUG, file_level:int =logging.DEBUG) -> logging.Logger:
    """
    Create a logger object with two type of formatted output: console and file.
    You can set different level of logging for each one. 
    Log file will be stored in passed log directory. The file name is the start execution datetime of the script.

    Args:
        log_path (str): Path of the directory to store the log files
        console_level (int): Level of logging for stdout(console). 
        file_level (int): Level of logging for file. 

    Returns:
        logging.Logger: Logger object instance
    """

    log_path = Path(log_path)
    if not log_path.is_dir():
        os.mkdir(log_path)
    creation_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(PurePath(log_path, f"{creation_time}.log"))
    c_handler.setLevel(console_level)
    f_handler.setLevel(file_level)
    c_format = logging.Formatter("%(asctime)s - %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
    f_format = logging.Formatter("%(asctime)s -  %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger