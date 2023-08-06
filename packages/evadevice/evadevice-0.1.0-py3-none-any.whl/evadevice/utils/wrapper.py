#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
from functools import wraps
from .logger import get_logger

logger = get_logger("evadevice")


def retry_wrapper(exception_handler=Exception, tries=3, delay=3):
    def _decorator(f):
        @wraps(f)
        def _decorated(*args, **kwargs):
            m_tries, m_delay = tries, delay
            while m_tries > 0:
                try:
                    return f(*args, **kwargs)
                except exception_handler as e:
                    logger.error(f"{e.args}, Retrying in {m_delay} seconds...")
                    time.sleep(m_delay)
                    m_tries -= 1
                    m_delay *= 2
            return f(*args, **kwargs)
        return _decorated
    return _decorator
