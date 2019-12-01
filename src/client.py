import xmlrpc.client
import logging

from api import *

def voting_process():
    # Create logger object
    logger = logger_factory('vote_process', 'voting.log', logging.ERROR)
    logger.info('Ready')

    # Picking voter informations (Name, CPF and Chosen Candidate)
    logger.info('Registering voter')
    name = input('Type your name: ')
    print()

    cpf = input('Type your CPF: ')
    print()

    voter = Voter(name, cpf)
    logger.info('voter '+str([cpf, name])+' registered')
    logger.info('voter '+str([cpf, name])+' starting voting')
    candidate = input('Type your chosen candidate: ')
    print()

    # Create Conection with Election Coordinator to Register Vote
    election_coordinator = xmlrpc.client.ServerProxy(RPC_SERVER_URI)
    try:
        print(election_coordinator.register_vote(candidate, voter))
        logger.info('Vote registered')

    except xmlrpc.client.ProtocolError as err:
        print("Error occurred")


if __name__ == '__main__':
    server = xmlrpc.client.ServerProxy(RPC_SERVER_URI)

    name = 'Lourenco'
    cpf = '000.000.000-00'
    candidate = 'Candidate A'

    server.register_vote(candidate, Voter(name, cpf))
