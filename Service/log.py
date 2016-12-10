import logging
import logging.handlers

def setup_logging(log_level="info", log_filename="ADSBackEndTask.log", console=True):
    """
    Configure logging system.

    Parameters
    ----------
    log_level : string
        Logging level such as debug, warn, info.
    log_filename : string
        Filename where to store the logs.
    console : boolean
        Print to screen too.

    Examples
    --------

    >>> setup_loging()
    >>> logging.info("Information")
    """
    # It is accessible via import logging; logging.warn("x")

    logger = logging.getLogger() # root logger, common for all
    #logger = logging.getLogger(name)
    logger.setLevel(logging.getLevelName(log_level.upper()))

    #formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s [%(funcName)s:%(lineno)d]: %(message)s')
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s:%(funcName)s:%(lineno)d]: %(message)s')
    #formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s')

    if console:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    megabyte = 1048576
    handler = logging.handlers.RotatingFileHandler(log_filename, 'a', maxBytes=50*megabyte, backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
