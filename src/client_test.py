from api import *
import xmlrpc.client

server = xmlrpc.client.ServerProxy(RPC_SERVER_URI)

name = 'Victor'
cpf = '000.000.000-04'
candidate = 'Test'

server.register_vote(candidate, Voter(name, cpf))
