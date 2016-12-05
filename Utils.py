class BidResponse(object):
    def __init__(self, buy=False, bid=0):
        self.buy = buy
        self.value = bid

    def __str__(self):
        return "buy:{} value:{}".format(self.buy, self.value)
