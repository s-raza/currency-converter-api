import logging


def get_logger(name: str, level: int = None) -> logging.Logger:
    """
    Utility function to get a logging instance to write logs to stdout.

    :param name: :obj:`str` Name of the logger to show in the output.
    :type str: required.

    :return: :obj:`logging.Logger`
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()

    if level is not None:
        console_handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)-2s] %(name)s: %(message)s",
        datefmt="%d-%b-%Y %I:%M:%S%p",
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
