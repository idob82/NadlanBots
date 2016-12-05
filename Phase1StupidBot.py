from Utils import BidResponse


class Phase1StupidBot(object):
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.cards = []

    def __str__(self):
        return "Stupid bot {}".format(self.name)

    def __repr__(self):
        return str(self)

    def init(self, money):
        self.money = money
        self.cards = []

    def bid(self, locations, previous_bids, current_bid):
        if len(locations) == 1 or current_bid >= self.money:
            return BidResponse(True)
        return BidResponse(bid=current_bid + 1)

    def buy(self, card, price):
        self.money -= price
        self.cards.append(card)

    def end_bidding_round(self):
        self.cards.sort()

    def bid_for_cheques(self, cheques_chosen):
        return self.cards[0]

    def buy_cheque(self, location, cheque, sorted_locations):
        self.money += cheque
        self.cards.remove(location)

    def end_buying_round(self):
        pass
