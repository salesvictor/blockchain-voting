from block import Block, Transaction
from blockchain import Blockchain
import api

NUMBER_CANDIDATES = 0

if __name__ == "__main__":

    blockchains = []

    NUMBER_CANDIDATES = 5

    for i in range(NUMBER_CANDIDATES):
        bc = Blockchain()
        blockchains.append(bc)

    blockchains[0].add_pending(Transaction('my_address', 'your_address', 'Vidal', '001.001.002-56'))
    blockchains[0].build_block()
    blockchains[1].add_pending(Transaction('your_address', 'my_address', 'Batata', '001.001.003-56'))
    blockchains[1].build_block()
    blockchains[2].add_pending(Transaction('your_address', 'other_address', 'Lourescasjjdascvhasdjvcsdnço', '001.031.002-56'))
    blockchains[2].build_block()
    blockchains[3].add_pending(
        Transaction('your_address', 'other_address', 'Lourescasjjdascvhasdjvcsdnço', '001.031.002-56'))
    blockchains[3].build_block()
    blockchains[4].add_pending(
        Transaction('your_address', 'other_address', 'Lourescasjjdascvhasdjvcsdnço', '001.031.002-56'))
    blockchains[4].build_block()

    for blockchain in blockchains:
        for block in blockchain.blockchain:
            print(block)
        print(len(blockchain.blockchain))