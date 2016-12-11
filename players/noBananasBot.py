import random

from playerbase import PlayerBase
from players_prototypes.RandomBotPrototype import RandomBotPrototype
from utils import BidResponse


class noBananasBot(RandomBotPrototype):
    def __init__(self):
        super(noBananasBot, self).__init__(0.6)

    def __str__(self):
        return "No Bananas Bot"
