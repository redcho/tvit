import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # logging.basicConfig(filename='app.log', filemode='w',
    #                     format='%(name)s - %(levelname)s - %(message)s')

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        logger.addHandler(ch)

    return logger
