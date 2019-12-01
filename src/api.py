import logging


RPC_SERVER_URI = 'localhost:8000'
RPC_SERVER_ADDR = ('localhost', 8000)
LOGGER_FORMATTER = logging.Formatter('[{asctime}|{name}|{levelname}] {message}',
                                      style='{')

class Voter:
    pass


def register_vote(candidate: str, voter: Voter):
    pass
