class BidResponse(object):
    def __init__(self, forfeit=False, bid=0):
        self.forfeit = forfeit
        self.value = bid
        assert (forfeit or (bid > 0))

    def __str__(self):
        return "BidResponse[forfeit:{}, value:{}]".format(self.forfeit, self.value)

    def __repr__(self):
        return str(self)


class PlayerState(object):
    def __init__(self):
        self.money = 0
        self.cards = []
        self.cheques = []

    def __str__(self):
        return "PlayerState[money:{}, cards:{}, cheques:{}]".format(self.money, self.cards, self.cheques)

    def __repr__(self):
        return str(self)


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

    def __str__(self):
        return "TurnStatus[player_id:{}, bid:{}, card:{}]".format(self.player_id, self.bid, self.card)

    def __repr__(self):
        return str(self)
