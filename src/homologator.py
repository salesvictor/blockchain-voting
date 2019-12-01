from block import Block, Transaction
from blockchain import Blockchain

if __name__ == "main":

    bc = Blockchain()
    print("kjbscjascbjksad")
    bc.add_pending(Transaction('my_address', 'your_address', 'Vidal', '001.001.002-56'))
    bc.add_pending(Transaction('your_address', 'my_address', 'Batata', '001.001.003-56'))
    bc.add_pending(Transaction('your_address', 'other_address', 'Lourenço', '001.031.002-56'))

    bc.build_block()

    for block in bc.blockchain:
        print(block)

    for address in ['my_address', 'your_address', 'other_address']:
        print(address, bc.check_balance(address))