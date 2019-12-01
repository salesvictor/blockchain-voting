import logging


RPC_SERVER_URI = 'localhost:8000'
RPC_SERVER_ADDR = ('localhost', 8000)


def logger_factory(name: str, filename: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    logger_formatter = logging.Formatter('[{asctime}|{name}|{levelname}] {message}',
                                         style='{')
    file_handler.setFormatter(logger_formatter)
    stream_handler.setFormatter(logger_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


class Voter:
    pass


def register_vote(candidate: str, voter: Voter):
    pass
