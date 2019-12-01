from block import Block, Transaction


class Blockchain:
    ''' Will hold a stream of blocks. '''

    def __init__(self):
        self.blockchain = [self.create_block()]
        self.pending_transactions = []

    def create_block(self):
        return Block([], previous_hash='0' * 64)

    def is_valid(self):
        for i in range(1, len(self.blockchain)):
            if self.blockchain[i].previous_hash != self.blockchain[i - 1].hash:
                return False

        return True

    def add_pending(self, transaction: Transaction):
        self.pending_transactions.append(transaction)

    def build_block(self):
        if len(self.pending_transactions) == 0:
            raise Exception('build_block: no transactions to build a block from')

        block = Block(self.pending_transactions, self.blockchain[-1].hash)
        self.pending_transactions = []
        self.blockchain.append(block)

    # Maybe it is useless for our application
    def check_balance(self, wallet_address: str):
        balance = 0

        for block in self.blockchain:
            for transaction in block.transactions:
                if transaction.from_address == wallet_address:
                    balance -= transaction.amount

                if transaction.to_address == wallet_address:
                    balance += transaction.amount

        return balance