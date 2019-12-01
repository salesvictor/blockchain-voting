from api import *
import xmlrpc.client
import xmlrpc.server
import logging


class CoordinatorService:
    votes = []
    homologators = []

    def register_vote(self, candidate: str, voter: Voter):
        logger = logging.getLogger('ElectionCoordinator')
        logger.info('Received vote')

        self.votes.append(Vote(candidate, voter))
        logger.info(self.votes)

    def add_homologator(port: int):
        logger = logging.getLogger('ElectionCoordinator')
        logger.info(f'New homologator on port {port}')

        homologator = xmlrpc.client.ServerProxy(f'https://localhost:{port}/')
        homologators.append(homologator)
        
        for vote in self.votes:
            homologator.homologate_vote(vote)


class ElectionCoordinator(xmlrpc.server.SimpleXMLRPCServer):
    def __init__(self, addr):
        super().__init__(addr, allow_none=True, logRequests=False)
        self.addr = addr
        self._register_services()
        self._create_logger()

    def start(self):
        self.logger.info('Listenning to connections')
        self.serve_forever()

    def _register_services(self):
        self.register_introspection_functions()
        self.register_instance(CoordinatorService())

    def _create_logger(self):
        self.logger = logger_factory('ElectionCoordinator',
                                     'ElectionCoordinator.log')
        self.logger.info('Ready')

