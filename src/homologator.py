from block import Block, Transaction
from threading import Thread
from blockchain import Blockchain
import xmlrpc.server
import logging
from random import randint
from api import *
import sys


class HomologatorService():
    def __init__(self):
        self.logger = logging.getLogger('Homologator')
        self.map_candidate = {'Candidate A': 0, 'Candidate B': 1, 'Candidate C': 2, 'Candidate D': 3, 'Candidate E': 4}
        self.blockchain_candidates = []
        self.number_candidates = 5
        for i in range(self.number_candidates):
            bc = Blockchain()
            self.blockchain_candidates.append(bc)

    def homologate_vote(self, vote: Vote):
        self.logger.info('Received vote to homologate')

        self.add_vote(vote)

        return 'Vote homologated'

    def map_vote(self, name_voter:str):
        return self.map_candidate[name_voter]

    def get_candidate_name(self, position):
        for name, val in self.map_candidate.items():
            if val == position:
                return name

    def add_vote(self, vote):
        candidate_position = self.map_vote(vote['candidate'])
        transaction = Transaction(vote['name'], vote['cpf'])
        self.blockchain_candidates[candidate_position].add_pending(transaction)
        self.blockchain_candidates[candidate_position].build_block()

    def get_election_winner(self):
        self.logger.info('Received request to send the winner of the election')

        max_chain_length = 0
        name_candidate = ''
        for blockchain_candidate in self.blockchain_candidates:
            if max_chain_length < len(blockchain_candidate.blockchain) - 1:
                max_chain_length = len(blockchain_candidate.blockchain) - 1
                name_candidate = self.get_candidate_name(max_chain_length)

        return name_candidate



class Homologator(xmlrpc.server.SimpleXMLRPCServer):
    def __init__(self, addr):
        super().__init__(addr, logRequests=False, allow_none=True)

        self.addr = addr
        self._register_functions()
        self._create_logger()

        server_thread = Thread(target=self.serve_forever)
        server_thread.start()

    def _register_functions(self):
        self.register_introspection_functions()
        self.register_instance(HomologatorService())

    def _create_logger(self):
        self.logger = logger_factory('Homologator',
                                     'Homologator.log')
        self.logger.info('Ready')


if __name__ == "__main__":
    port = int(sys.argv[1])
    homologator = Homologator(addr=('localhost', port))
    election_coordinator = xmlrpc.client.ServerProxy(RPC_SERVER_URI)
    try:
        election_coordinator.add_homologator(port)
    except xmlrpc.client.ProtocolError as err:
        print("Error occurred")
