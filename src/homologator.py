from block import Block, Transaction
from blockchain import Blockchain
import xmlrpc.server
import xmlrpc.client
import logging
import threading
from random import randint
from api import *
import sys


class Homologator(xmlrpc.server.SimpleXMLRPCServer):
    def __init__(self, addr):
        super().__init__(addr, logRequests=False, allow_none=True)
        self.addr = addr
        self.shutdown_condition = threading.Condition()
        self.shutdown_event = threading.Event()
        self._register_functions()
        self._create_logger()

    def start(self):
        self.server_thread = threading.Thread(target=self.serve_forever)
        self.server_thread.start()

    def serve_forever(self):
        base_thread = threading.Thread(target=super().serve_forever)
        base_thread.start()

        with self.shutdown_condition:
            self.shutdown_condition.wait_for(self.shutdown_event.is_set)
        self.shutdown()

    def shutdown(self):
        self.logger.info('Shutting down')
        super().shutdown()
        self.logger.info('Shutdown successfull')

    def _register_functions(self):
        self.register_introspection_functions()
        self.register_instance(HomologatorService(self))

    def _create_logger(self):
        self.logger = logger_factory('Homologator',
                                     'Homologator.log')
        self.logger.info('Ready')


class HomologatorService:
    def __init__(self, homologator: Homologator):
        self.homologator = homologator
        self.port = self.homologator.addr[1]
        self.logger = logging.getLogger('Homologator')
        self.candidates = []
        self.candidate_number = dict()
        self.candidate_parties = dict()
        self._get_candidates()
        self.blockchain_candidates = []
        self.number_candidates = len(self.candidate_number)
        for i in range(self.number_candidates):
            bc = Blockchain(i)
            self.blockchain_candidates.append(bc)

    def shutdown(self):
        self.logger.info('Setting shutdown event')
        self.homologator.shutdown_event.set()
        with self.homologator.shutdown_condition:
            self.homologator.shutdown_condition.notify()

    def homologate_vote(self, vote: Vote):
        self.logger.info('Received vote to homologate')

        self.add_vote(vote)

        return 'Vote homologated'

    def add_vote(self, vote):
        candidate_position = self.candidate_number[vote['candidate']]
        transaction = Transaction(vote['name'], vote['cpf'])
        self.blockchain_candidates[candidate_position].add_pending(transaction)
        self.blockchain_candidates[candidate_position].build_block()

    def show_all_blockchains(self):
        for blockchain_candidate in self.blockchain_candidates:
            for block in blockchain_candidate.blockchain:
                print(block)
            print(len(blockchain_candidate.blockchain))

    def get_election_winner(self):
        self.logger.info('Received request to send the winner of the election')

        max_chain_length = 0
        name_candidate = ''

        for blockchain_candidate in self.blockchain_candidates:
            if (max_chain_length < len(blockchain_candidate.blockchain) - 1) and blockchain_candidate.is_valid():
                max_chain_length = len(blockchain_candidate.blockchain) - 1
                name_candidate = self.candidates[blockchain_candidate.id][0]

        return name_candidate

    def pass_blockchains_to_new_homologator(self, candidate: int):
        self.logger.info('Pass the candidate\'s blockchain to a new homologator')

        return [block.transactions for block in self.blockchain_candidates[candidate].blockchain]

    def pass_ports(self, ports: list):
        old_homologators = []
        for port in ports:
            old_homologator = xmlrpc.client.ServerProxy(f'http://localhost:{port}')
            old_homologators.append(old_homologator)
        for candidate in range(self.number_candidates):
            blockchain_candidate = []
            for old_homologator in old_homologators:
                print(old_homologator)
                list_transaction = old_homologator.pass_blockchains_to_new_homologator(candidate)
                print('kdjksjdc')
                bc = Blockchain(candidate)
                bc.copy_blocks(list_transaction)
                print('kdjksjdc')
                blockchain_candidate.append(bc)
            blockchain_candidate = [bc for bc in blockchain_candidate if bc.is_valid()]
            biggest_size = max([len(bc.blockchain) for bc in blockchain_candidate])
            blockchain_candidate = [bc for bc in blockchain_candidate if len(bc.blockchain) == biggest_size]
            self.blockchain_candidates[candidate] = blockchain_candidate[0]



    def _get_candidates(self):
        file = open('candidates.csv', 'r')
        for idx, line in enumerate(file.readlines()[1:]):
            candidate, party = line.split(',')
            self.candidates.append((candidate, party))
            self.candidate_number[candidate] = idx
            self.candidate_parties[candidate] = party

if __name__ == "__main__":
    port = int(sys.argv[1])
    homologator = Homologator(addr=('localhost', port))
    homologator.start()
    election_coordinator = xmlrpc.client.ServerProxy(RPC_SERVER_URI)
    try:
        election_coordinator.add_homologator(port)
    except xmlrpc.client.ProtocolError as err:
        print("Error occurred")
