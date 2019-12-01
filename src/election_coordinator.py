from api import *
import xmlrpc.server
import logging


def register_vote(candidate: str, voter: Voter):
    logger = logging.getLogger('ElectionCoordinator')
    logger.info('Received vote')

    return 'Vote received successfully'


class ElectionCoordinator(xmlrpc.server.SimpleXMLRPCServer):
    def __init__(self, addr):
        super().__init__(addr, allow_none=True)
        self.addr = addr
        self._register_functions()
        self._create_logger()

    def start(self):
        self.logger.info('Listenning to connections')
        self.serve_forever()

    def _register_functions(self):
        self.register_introspection_functions()
        self.register_function(register_vote)

    def _create_logger(self):
        self.logger = logger_factory('ElectionCoordinator',
                                     'ElectionCoordinator.log')
        self.logger.info('Ready')

