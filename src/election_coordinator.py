from api import *
import logging
import re
import threading
import xmlrpc.client
import xmlrpc.server


class CoordinatorService:
    def __init__(self):
        self.allowed_voters_data = []
        self.homologators = []
        self.votes = []
        self._load_data()

    def register_vote(self, candidate: str, voter: Voter):
        logger = logging.getLogger('ElectionCoordinator')
        logger.info('Received vote')

        answer = self._authentication(voter)
        if answer == 'Successful Authentication':
            pattern_cpf, _ = self._is_valid_cpf(voter['cpf'])
            pattern_name = voter['name'].upper()
            current_voter_index = 0
            for allowed_voter_data in self.allowed_voters_data:
                if allowed_voter_data[0] == pattern_name and allowed_voter_data[1] == pattern_cpf:
                    voter_index = current_voter_index
                current_voter_index += 1
            pattern_candidate = candidate.upper()
            vote = Vote(Voter(pattern_name, pattern_cpf), pattern_candidate)
            vote_weight = self.allowed_voters_data[voter_index][2]
            for i in range(vote_weight):
                self.votes.append(vote)
                for homologator in self.homologators:
                        homologator.homologate_vote(vote)

            logger.info(f'Vote CPF is {vote.cpf}')
            logger.info(f'Vote Weight is {str(vote_weight)}')

            return 'Vote received successfully'
        else:
            logger.info(answer)
            logger.info('Reporting client!')
            return answer

    def add_homologator(self, port: int):
        logger = logging.getLogger('ElectionCoordinator')
        logger.info(f'New homologator on port {port}')

        homologator = xmlrpc.client.ServerProxy(f'http://localhost:{port}/')
        self.homologators.append(homologator)
        
        for vote in self.votes:
            homologator.homologate_vote(vote)

    def _is_valid_cpf(self, cpf: str):
        prog = re.compile('[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}$')
        result = prog.match(cpf)
        if result: #CPF correctly formatted
            return cpf, True
        return None, False

    def _authentication(self, voter: Voter):
        # Checking if CPF is valid
        voter_cpf, is_valid_cpf = self._is_valid_cpf(voter['cpf'])
        if not is_valid_cpf:
            return f'Wrong CPF Format. Expected xxx.xxx.xxx-xx and received {voter_cpf}'


        # Searching voter's identity at allowed voters database
        voter_name = voter['name']
        for allowed_voter_data in self.allowed_voters_data:
            if allowed_voter_data[0] == voter_name and allowed_voter_data[1] == voter_cpf:
                return 'Successful Authentication'

        # If it comes until here, then voter's name or CPF was not found at the Database
        name_flag = False
        cpf_flag = False
        for i in range(len(self.allowed_voters_data)):
            if self.allowed_voters_data[i][0] == voter_name:
                name_flag = True
            if self.allowed_voters_data[i][1] != voter_cpf:
                cpf_flag = True
        if not name_flag:
            return 'Given name not in database of allowed voters'
        elif not cpf_flag:
           return 'Given CPF not in database of allowed voters'
        else:
            return 'Given pair (Name, CPF) not in database of allowed voters'

    def _load_data(self):
        allowed_voters = open('allowed_voters.txt', 'r')
        for line in allowed_voters.readlines():
            allowed_voter_data = line.split(',')
            allowed_voter_data[2] = int(allowed_voter_data[2].replace('\n', ''))
            self.allowed_voters_data.append(allowed_voter_data)


class ElectionCoordinator(xmlrpc.server.SimpleXMLRPCServer):
    def __init__(self, addr: tuple = RPC_SERVER_ADDR, timeout: int = 10):
        super().__init__(addr, allow_none=True, logRequests=False)
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
        self.logger.info('Shutting down')
        super().shutdown()
        self.logger.info('Server is down')

        winners = []
        for homologator in self.service.homologators:
            winners.append(homologator.get_election_winner())

        self.logger.info(f'Winners found: {winners}')

        for homologator in self.service.homologators:
            self.logger.debug(f'Shutting down homologator {homologator}')
            homologator.shutdown()

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
