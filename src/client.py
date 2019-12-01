import xmlrpc.client
import logging

from api import *

def voting_process():
    # create logger object
    logger = logger_factory('vote_process', 'voting.log', logging.ERROR)

    logger.info('registering voter')
    name = input('Type your name: ')
    print()

    cpf = input('Type your CPF: ')
    print()

    voter = Voter(cpf, name)
    logger.info('voter '+str([cpf, name])+' registered')
    logger.info('voter '+str([cpf, name])+' starting voting')
    candidate = input('Type your chosen candidate: ')
    print()

    logger.info('vote registered')

    election_coordinator = xmlrpc.client.ServerProxy(RPC_SERVER_URI)
    try:
        print(election_coordinator.register_vote(candidate, voter))
    except xmlrpc.client.ProtocolError as err:
        print("Error occurred")
