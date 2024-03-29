import logging


RPC_SERVER_URI = 'http://localhost:8000/'
RPC_SERVER_ADDR = ('localhost', 8000)


def logger_factory(name: str, filename: str, stream_level: int = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(f'log/{filename}')
    file_handler.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(stream_level)
    logger_formatter = logging.Formatter('[{asctime}|{name}|{levelname}] {message}',
                                         style='{')
    file_handler.setFormatter(logger_formatter)
    stream_handler.setFormatter(logger_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


class Voter:
    def __init__(self, name: str, cpf:str):
        self.name = name
        self.cpf = cpf


class Vote:
    def __init__(self, voter: Voter, candidate: str):
        self.name = voter.name
        self.cpf = voter.cpf
        self.candidate = candidate
