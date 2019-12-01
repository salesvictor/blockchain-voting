import xmlrpc.client
import logging

from api import *

def do_something():
    tkinter.messagebox.showinfo('Response', 'You have clicked the Button')

def vote_interface():
    root = tkinter.Tk()


    label = tkinter.Label(root, text = 'Hello World')
    another_label = tkinter.Label(root, text = 'This is GUI')
    label.pack()
    another_label.pack()
    root.mainloop()
    button = tkinter.Button(root, text="Click Me", command = do_something)
    button.pack()


if __name__ == "__main__":
    #vote_interface()

    # create logger object
    logger = logger_factory('vote_process', 'voting.log', logging.ERROR)

    logger.info('registering voter')
    nome = input('Digite seu nome: ')
    print()

    cpf = input('Digite seu cpf: ')
    print()

    voter = Voter(cpf, nome)
    logger.info('voter '+str([cpf, nome])+' registered')
    logger.info('voter '+str([cpf, nome])+' starting voting')
    candidate = input('Digite seu candidato: ')
    print()

    logger.info('vote registered')

    election_coordinator = xmlrpc.client.ServerProxy(RPC_SERVER_URI)
    try:
        election_coordinator.register_vote(candidate, voter)
    except xmlrpc.client.ProtocolError as err:
        print("Error occurred")
