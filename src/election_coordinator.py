from api import *
import xmlrpc.server
import logging


class ElectionCoordinator(xmlrpc.server.SimpleXMLRPCServer):
    def __init__(self, addr):
        super().__init__(addr)
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
        self.logger = logging.getLogger('ElectionCoordinator')
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('ElectionCoordinator.log')
        file_handler.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logger_formatter)
        stream_handler.setFormatter(logger_formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        self.logger.info('Ready')

