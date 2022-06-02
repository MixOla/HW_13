import logging


def create_logger():

    logger = logging.getLogger('basic')
    logger.setLevel("DEBUG")

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("logs/basic.log", encoding="utf-8")

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Добавляем форматтеры
    formatter_one = logging.Formatter("%(asctime)s : %(message)s")

    console_handler.setFormatter(formatter_one)
    file_handler.setFormatter(formatter_one)