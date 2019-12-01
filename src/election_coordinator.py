from api import *
import logging
import re
import threading
import xmlrpc.client
import xmlrpc.server


class CoordinatorService:
    votes = []
    homologators = []

    def register_vote(self, candidate: str, voter: Voter):
        logger = logging.getLogger('ElectionCoordinator')
        logger.info('Received vote')

        vote, answer, vote_weight = self._authentication(candidate, voter)

        if vote is not None:
            for i in range(vote_weight):
                self.votes.append(vote)
                for homologator in self.homologators:
                        homologator.homologate_vote(vote)

            logger.info('Vote CPF is ' + vote.cpf)
            logger.info('Vote Weight is ' + str(vote_weight))

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
            return True
        return False

    def _authentication(self, candidate: str, voter: Voter):
        allowed_voters = open("allowed_voters.txt", "r")

        # Format voter data
        voter_name = voter['name'].upper()
        voter_candidate = candidate.upper()
        voter_cpf = voter['cpf']
        if not self._is_valid_cpf(voter_cpf):
            return None, f'Wrong CPF Format. Expected xxx.xxx.xxx-xx and received {voter_cpf}', None

        # Sending information
        counter = 0
        allowed_voters_data = []
        for line in allowed_voters.readlines():
            counter = counter + 1
            allowed_voter_data = line.split(',')
            allowed_voter_data[2] = allowed_voter_data[2].replace('\n', '')
            allowed_voters_data.append(allowed_voter_data)
            if allowed_voter_data[0] == voter_name and allowed_voter_data[1] == voter_cpf:
                authenticated_voter = Voter(voter_cpf, voter_name)
                return Vote(authenticated_voter, voter_candidate), 'Successful Authentication', int(allowed_voter_data[2])

        name_flag = False
        cpf_flag = False
        for i in range(counter):
            if allowed_voters_data[i][0] == voter_name:
                name_flag = True
            if allowed_voters_data[i][1] != voter_cpf:
                cpf_flag = True
        if not name_flag:
            return None, 'Given name not in database of allowed voters', None
        elif not cpf_flag:
            return None, 'Given CPF not in database of allowed voters', None


class ElectionCoordinator(xmlrpc.server.SimpleXMLRPCServer):
    def __init__(self, addr: tuple = RPC_SERVER_ADDR, timeout: int = 10):
        super().__init__(addr, allow_none=True, logRequests=False)
        self.addr = addr
        self.timeout = timeout
        self._register_services()
        self._create_logger()

    def start(self):
        self.logger.info('Listenning to connections')
        serving_thread = threading.Thread(target=self.serve_forever)
        serving_thread.start()
        serving_thread.join(timeout=self.timeout)
        
        self.logger.info('Election time has run out')
        self.shutdown()

    def _register_services(self):
        self.register_introspection_functions()
        self.register_instance(CoordinatorService())

    def _create_logger(self):
        self.logger = logger_factory('ElectionCoordinator',
                                     'ElectionCoordinator.log')
        self.logger.info('Ready')

