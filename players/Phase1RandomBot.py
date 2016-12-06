from utils import BidResponse
import random

from players.playerbase import PlayerBase


class Phase1RandomBot(PlayerBase):
    def __init__(self):
        super(Phase1RandomBot, self).__init__()
        self.random_level = 0.4

    def __str__(self):
        return "Random bot"

    def init(self, money):
        self.money = money
        self.cards = []

    def bid(self, locations, previous_bids, current_bid):
        if len(locations) == 1 or current_bid >= self.money or random.random() < self.random_level:
            return BidResponse(True)
        return BidResponse(bid=current_bid + 1)

    def buy(self, card, price):
        self.money -= price
        self.cards.append(card)

    def end_bidding_round(self):
        self.cards.sort()

    def bid_for_cheques(self, cheques_chosen):
        if random.random() < self.random_level:
            self.cards[random.randint(0, len(self.cards) - 1)]
        return self.cards[0]

    def buy_cheque(self, location, cheque, sorted_locations):
        self.money += cheque
        self.cards.remove(location)

    def end_buying_round(self):
        pass
