import logging

instance = None


def get_logger():
    global instance
    if not instance:
        instance = logging.getLogger("pyutrack")
    return instance
