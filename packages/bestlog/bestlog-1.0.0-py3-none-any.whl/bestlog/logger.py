import logging
import sys
from logging import handlers
import os


class setting:
    log_level = logging.INFO
    log_path = "./logs"

def get(loger_name, tag = "default") -> logging.LoggerAdapter:
    log = logging.getLogger(loger_name)
    log = logging.LoggerAdapter(log, {"tag": tag})
    log.setLevel(setting.log_level)
    return log

def init(loger_name: str, tag = False, to_stdout = True, to_file = True, backup_days = 0):
    if to_stdout:
        handler = logging.StreamHandler(sys.stdout)
        if tag:
            logging_format = logging.Formatter("[%(asctime)s][%(levelname)s][%(tag)s]: %(message)s")
        else:
            logging_format = logging.Formatter("[%(asctime)s][%(levelname)s]: %(message)s")
        handler.setFormatter(logging_format)
        logging.getLogger(loger_name).addHandler(handler)
    if to_file:
        if not os.path.exists(setting.log_path):
            os.makedirs(setting.log_path)
        log_file_name = "{0}.log".format(loger_name)
        log_file_path = os.path.join(setting.log_path, log_file_name)
        handler = logging.handlers.TimedRotatingFileHandler(log_file_path, when="midnight", encoding='UTF-8',
                                                            backupCount=backup_days)
        handler.suffix = "%Y-%m-%d"
        handler.setFormatter(logging_format)
        logging.getLogger(loger_name).addHandler(handler)

