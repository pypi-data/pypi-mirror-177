import logging
import sys
from logging import handlers
import os


default_log_level = logging.INFO
default_log_path = "./logs"
default_backup_days = 0


def get(loger_name, tag = "default") -> logging.LoggerAdapter:
    log = logging.getLogger(loger_name)
    log = logging.LoggerAdapter(log, {"tag": tag})
    return log


def init(loger_name: str, tag: bool = False, to_stdout: bool = True, to_file: bool = True, log_path: str = None,
         log_level: int = None, backup_days: int = None):

    if log_path is None:
        log_path = default_log_path
    if log_level is None:
        log_level = default_log_level
    if backup_days is None:
        backup_days = default_backup_days
    logging.getLogger(loger_name).setLevel(log_level)

    if to_stdout:
        handler = logging.StreamHandler(sys.stdout)
        if tag:
            logging_format = logging.Formatter("[%(asctime)s][%(levelname)s][%(tag)s]: %(message)s")
        else:
            logging_format = logging.Formatter("[%(asctime)s][%(levelname)s]: %(message)s")
        handler.setFormatter(logging_format)
        logging.getLogger(loger_name).addHandler(handler)
    if to_file:
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_file_name = "{0}.log".format(loger_name)
        log_file_path = os.path.join(log_path, log_file_name)
        handler = logging.handlers.TimedRotatingFileHandler(log_file_path, when="midnight", encoding='UTF-8',
                                                            backupCount=backup_days)
        handler.suffix = "%Y-%m-%d"
        handler.setFormatter(logging_format)
        logging.getLogger(loger_name).addHandler(handler)


