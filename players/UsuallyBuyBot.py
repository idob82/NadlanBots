import random

from playerbase import PlayerBase
from players_prototypes.RandomBotPrototype import RandomBotPrototype
from utils import BidResponse


class UsuallyBuyBot(RandomBotPrototype):
    def __init__(self):
        super(UsuallyBuyBot, self).__init__(0.6)

    def __str__(self):
        return "Usually Buy Bot"
