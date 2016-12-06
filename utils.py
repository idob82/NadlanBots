class BidResponse(object):
    def __init__(self, buy=False, bid=0):
        self.buy = buy
        self.value = bid

    def __str__(self):
        return "buy:{} value:{}".format(self.buy, self.value)


class PlayerState(object):
    def __init__(self):
        self.money = 0
        self.cards = []
        self.cheques = []


class TurnStatus(object):
    def __init__(self, player_id, bid, card):
        """
        :type player_id: str
        :type bid: int
        :type card: int
        """
        self.player_id = player_id
        self.bid = bid
        self.card = card
