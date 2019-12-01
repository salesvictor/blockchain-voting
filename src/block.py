import hashlib


class Transaction:
    def __init__(self, name: str, cpf: str):
        self.name = name
        self.cpf = cpf

class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, transactions: list, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash

    def print_previous_hash(self):
        print(self.previous_hash)

    @property
    def hash(self):
        h = hashlib.sha256()
        h.update(bytes(str(self.transactions), 'utf8'))
        h.update(bytes(self.previous_hash, 'ascii'))
        return h.hexdigest()

    def __repr__(self):
        return f'Block transactions={self.transactions} hash={self.hash[-1:]}'