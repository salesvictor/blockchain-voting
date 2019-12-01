import xmlrpc.client
import logging
import re

from api import *

class Client:
    def __init__(self):
        self._create_logger()

    def _create_logger(self):
        self.logger = logger_factory('vote_process', 'voting.log')
        self.logger.info('Ready')

    def _standardize_cpf(self, cpf: str):
        prog = re.compile('[0-9]{3}\.[0-9]{3}\.[0-9]{3}\-[0-9]{2}$')
        result = prog.match(cpf)
        if result:
            #CPF correctly formatted
            return cpf
        else: 
            # Or just numbers were given or the information is wrong. At both 
            # cases, standardize the cpf and let the election coordinator
            # authenticate
            if len(cpf) < 11:
                cpf = cpf.zfill(11)
            cpf = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
            return cpf

    def _standardize_name(self, name: str):
        return name.upper()

    def voting_process(self, given_information : bool, name : str = None, 
                       cpf: str = None, candidate: str = None):
        # Picking voter informations (Name, CPF)
        self.logger.info('Start voting process')
        if not given_information:
            name = input('Type your name: ')
            print()

            cpf = input('Type your CPF: ')
            print()

        # Standardize voter's name and cpf
        name = self._standardize_name(name)
        cpf = self._standardize_cpf(cpf)

        # Create object Voter to register vote
        voter = Voter(name, cpf)
        self.logger.info(f'voter {str([cpf, name])} registered')

        # Beginning of the Election
        self.logger.info(f'voter {str([cpf, name])} starting votation')

        if not given_information:
            candidate = input('Type your chosen candidate: ')
            print()

        candidate = self._standardize_name(candidate)

        # Create Conection with Election Coordinator to Register Vote
        election_coordinator = xmlrpc.client.ServerProxy(RPC_SERVER_URI)
        try:
            register_status = election_coordinator.register_vote(candidate, 
                                                                 voter)
            if register_status == 'Vote received successfully':
                self.logger.info('Vote successfully registered')
            else:
                self.logger.info(f'Following error occurred:{register_status}')

        except xmlrpc.client.ProtocolError as err:
            print(f'Error occurred: {str(err)}')


if __name__ == '__main__':
    # Voter Information
    name = 'Lourenco'
    cpf = '00000000000'
    candidate = 'C1'

    # Calling Client Interface to start voting process
    client = Client()
    client.voting_process(True, name, cpf, candidate)

    name = 'Victor'
    cpf = '00000000004'
    candidate = 'C2'
    client.voting_process(True, name, cpf, candidate)
