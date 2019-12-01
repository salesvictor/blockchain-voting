from block import Block, Transaction
from blockchain import Blockchain
from random import randint
import api

NUMBER_CANDIDATES = 1

class Homologator():
    def __init__(self, number_candidates: int):
        self.dict = {'Candidate A': 0, 'Candidate B': 1, 'Candidate C': 2, 'Candidate D': 3, 'Candidate E': 4}
        self.number_candidates = number_candidates
        self.blockchain_candidates = []
        for i in range(self.number_candidates):
            bc = Blockchain()
            self.blockchain_candidates.append(bc)

    def map_vote(self, name_voter:str):
        return self.dict[name_voter]

    def get_candidate_name(self, position):
        for name,val in self.dict.items():
            if val == position:
                return name

    def add_vote(self, vote):
        candidate_position = self.map_vote(vote.get_candidate_name())
        self.blockchain_candidates[candidate_position].add_pending(vote.get_content())
        self.blockchain_candidates[candidate_position].build_block()

    def get_winner_election(self):
        max = 0
        name_candidate = ''
        for blockchain_candidate in self.blockchain_candidates:
            if max < len(blockchain_candidate.blockchain)-1:
                max = len(blockchain_candidate.blockchain)
                name_candidate = self.get_candidate_name(max)

        return name_candidate


if __name__ == "__main__":

    homolagator = Homologator(2)