__version__ = "0.1.2"

import logging
from logutils.consts import (
    lila, lime_green, grey, yellow, blue, red, bold_red, sand, reset, background_red
)


class CustomFormatter(logging.Formatter):
    def __init__(self, colored):
        self.colored = colored

    def get_fmt_string(self, level):
        if self.colored:
            time_fmt = f"{lime_green}[%(asctime)s]{reset}"
            location_fmt = f"{lila}%(filename)s:%(funcName)s:%(lineno)d{reset}"
            match level:
                case logging.DEBUG:
                    level_fmt = f"{grey}%(levelname)s{reset}"
                    message_fmt = f"{sand}%(message)s{reset}"
                case logging.INFO:
                    level_fmt = f"{blue}%(levelname)s{reset}"
                    message_fmt = f"{sand}%(message)s{reset}"
                case logging.WARNING:
                    level_fmt = f"{yellow}%(levelname)s{reset}"
                    message_fmt = f"{sand}%(message)s{reset}"
                case logging.ERROR:
                    level_fmt = f"{red}%(levelname)s{reset}"
                    message_fmt = f"{red}%(message)s{reset}"
                case logging.CRITICAL:
                    level_fmt = f"{background_red}{sand}%(levelname)s{reset}{reset}"
                    message_fmt = f"{background_red}{sand}%(message)s{reset}{reset}"
                case _:
                    raise Exception("Wrong log level")
        else:
            time_fmt = "[%(asctime)s]"
            level_fmt = "%(levelname)s"
            message_fmt = "%(message)s"
            location_fmt = "%(filename)s:%(funcName)s:%(lineno)d"
        fmt = f"{time_fmt} | {level_fmt} | {location_fmt} | {message_fmt}"
        return fmt

    def format(self, record):
        log_fmt = self.get_fmt_string(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name, level=logging.INFO, handler_type="stream", propagate=False):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    match handler_type:
        case "stream":
            handler = logging.StreamHandler()
        case _:
            raise Exception(f"Handler {handler_type} not supported")
    if level not in (
        logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
    ):
        raise Exception(f"Level {level} not supported")
    handler.setLevel(level)
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    logger.propagate = propagate
    return logger
