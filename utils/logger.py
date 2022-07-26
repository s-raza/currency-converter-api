import logging


def get_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)-2s] %(name)s: %(message)s",
        datefmt="%d-%b-%Y %I:%M:%S%p",
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
