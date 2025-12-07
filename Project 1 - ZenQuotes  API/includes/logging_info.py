import logging


def logging_config():
    logging.basicConfig(
    filename="quotes_mailer.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",)

    return logging.getLogger(__name__)