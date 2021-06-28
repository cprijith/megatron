import logging

@staticmethod
def get_logger(name='', level=''):
    logger = logging.getLogger(name if name else 'ROOT')
    if name and level:
        logger.setLevel(level=level)
    else:
        logger.warning("ignoring level since logger name is not explicit, level: {}, name: {}".format(level, name))
    return logger


