from api import *
import xmlrpc.server
import logging
import re

def authentication(candidate: str, voter: Voter):
    allowed_voters = open("allowed_voters.txt", "r")

    # Format voter data
    voter_name = voter['name'].upper()
    voter_candidate = candidate.upper()
    voter_cpf = voter['cpf']
    if voter_cpf.isdigit(): #just numbers
        if len(voter_cpf) < 11:
            voter_cpf = voter_cpf.zfill(11)
        voter_cpf = '{}.{}.{}-{}'.format(voter_cpf[:3], voter_cpf[3:6], voter_cpf[6:9], voter_cpf[9:])
    prog = re.compile('[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}')
    result = prog.match(voter_cpf)
    if result: #CPF correctly formatted
        pass
    else:
        return None,'Wrong CPF Format. Expected xxx.xxx.xxx-xx and received '+voter_cpf, None

    # Sending information
    for line in allowed_voters.readlines():
        allowed_voter_data = line.split(',')
        allowed_voter_data[2] = allowed_voter_data[2].replace('\n', '')
        if allowed_voter_data[0] == voter_name and allowed_voter_data[1] == voter_cpf:
            authenticated_voter = Voter(voter_cpf, voter_name)
            return Vote(authenticated_voter, voter_candidate), 'Successful Authentication', int(allowed_voter_data[2])
        else:
            if allowed_voter_data[0] != voter_name:
                return None, 'Given name not in database of allowed voters', None
            if allowed_voter_data[1] != voter_cpf:
                return None, 'Given CPF not in database of allowed voters', None


def register_vote(candidate: str, voter: Voter):
    logger = logging.getLogger('ElectionCoordinator')
    logger.info('Received vote')

    vote, answer, vote_weight = authentication(candidate, voter)

    if vote is not None:
        # for i in range(vote_weight):
        #    pass
        logger.info('Vote CPF is ' + vote.voter.cpf)
        logger.info('Vote Weight is ' + str(vote_weight))
        return 'Vote received successfully'
    else:
        return answer


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

