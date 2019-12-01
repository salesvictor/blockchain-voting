from api import *
import logging
import re
import threading
import xmlrpc.client
import xmlrpc.server


class CoordinatorService:
    votes = []
    homologators = []

    def __init__(self):
        self.voters_voting_weights = []
        self.picking_weights()

    def picking_weights(self):
        self.allowed_voters = open("allowed_voters.txt", "r")
        for line in self.allowed_voters.readlines():
            allowed_voter_data = line.split(',')
            allowed_voter_data[2] = allowed_voter_data[2].replace('\n', '')
            self.voters_voting_weights.append(allowed_voter_data[2])

    def register_vote(self, candidate: str, voter: Voter):
        logger = logging.getLogger('ElectionCoordinator')
        logger.info('Received vote')

        voter_index, answer = self._authentication(candidate, voter)

        if voter_index is not None:
            pattern_cpf, _ = self._is_valid_cpf(voter['cpf'])
            pattern_name = voter['name'].upper()
            pattern_candidate = candidate.upper()
            vote = Vote(Voter(pattern_name, pattern_cpf), pattern_candidate)
            vote_weight = self.voters_voting_weights[voter_index]
            for i in range(vote_weight):
                self.votes.append(vote)
                for homologator in self.homologators:
                        homologator.homologate_vote(vote)

            logger.info(f'Vote CPF is {vote.cpf}')
            logger.info(f'Vote Weight is {str(vote_weight)}')

            return 'Vote received successfully'
        else:
            logger.info('An error occurred')
            return answer

    def add_homologator(self, port: int):
        logger = logging.getLogger('ElectionCoordinator')
        logger.info(f'New homologator on port {port}')

        homologator = xmlrpc.client.ServerProxy(f'http://localhost:{port}/')
        self.homologators.append(homologator)
        
        for vote in self.votes:
            homologator.homologate_vote(vote)

    def _is_valid_cpf(self, cpf: str):
        if cpf.isdigit(): #just numbers
            if len(cpf) < 11:
                cpf = cpf.zfill(11)
            cpf = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        prog = re.compile('[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}$')
        result = prog.match(cpf)
        if result: #CPF correctly formatted
            return cpf, True
        return None, False

    def _authentication(self, candidate: str, voter: Voter):
        # Format voter data
        voter_name = voter['name'].upper()
        voter_cpf = voter['cpf']
        voter_cpf, is_valid_cpf = self._is_valid_cpf(voter_cpf)
        if not is_valid_cpf:
            return None, f'Wrong CPF Format. Expected xxx.xxx.xxx-xx and received {voter_cpf}'

        # Sending information
        n_allowed_voters = 0
        allowed_voters_data = []
        for line in self.allowed_voters.readlines():
            allowed_voter_data = line.split(',')
            allowed_voters_data.append(allowed_voter_data[:2])
            if allowed_voter_data[0] == voter_name and allowed_voter_data[1] == voter_cpf:
                return n_allowed_voters, 'Successful Authentication'
            n_allowed_voters = n_allowed_voters + 1

        name_flag = False
        cpf_flag = False
        for i in range(n_allowed_voters):
            if allowed_voters_data[i][0] == voter_name:
                name_flag = True
            if allowed_voters_data[i][1] != voter_cpf:
                cpf_flag = True
        if not name_flag:
            return None, 'Given name not in database of allowed voters'
        elif not cpf_flag:
           return None, 'Given CPF not in database of allowed voters'


class ElectionCoordinator(xmlrpc.server.SimpleXMLRPCServer):
    def __init__(self, addr: tuple = RPC_SERVER_ADDR, timeout: int = 60):
        super().__init__(addr, allow_none=True, logRequests=False)
        self.addr = addr
        self.timeout = timeout
        self.service = CoordinatorService()
        self._register_services()
        self._create_logger()

    def start(self):
        self.logger.info('Listenning to connections')
        serving_thread = threading.Thread(target=self.serve_forever)
        serving_thread.start()
        serving_thread.join(timeout=self.timeout)
        
        self.logger.info('Election time has run out, shutting RPC down')
        self.shutdown()

    def shutdown(self):
        super().shutdown()
        self.logger.info('Servers are down')

        winners = []
        for homologator in self.service.homologators:
            winners.append(homologator.get_election_winner())

        self.logger.info(f'Winners found: {winners}')

    def _register_services(self):
        self.register_introspection_functions()
        self.register_instance(self.service)

    def _create_logger(self):
        self.logger = logger_factory('ElectionCoordinator',
                                     'ElectionCoordinator.log')
        self.logger.info('Ready')


if __name__ == '__main__':
    coordinator = ElectionCoordinator(RPC_SERVER_ADDR)
    coordinator.start()
