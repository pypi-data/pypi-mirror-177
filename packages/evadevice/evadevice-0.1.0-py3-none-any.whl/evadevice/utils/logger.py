#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging


def init_logging():
    """Initializes logger."""

    airtest_logger = logging.getLogger("airtest")
    airtest_logger.setLevel(logging.FATAL)
    # init evadevice logger
    logger = logging.getLogger("evadevice")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="[%(asctime)s][%(levelname)s]<%(name)s> %(message)s",
        datefmt="%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


init_logging()


def get_logger(name):
    """Return a logger with the specified name, creating it if necessary.

    :param name: logger name.
    """
    logger = logging.getLogger(name)
    return logger
