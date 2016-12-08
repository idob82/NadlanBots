import random

from playerbase import PlayerBase
from utils import BidResponse


class Phase1RandomBot(PlayerBase):
    def __init__(self):
        super(Phase1RandomBot, self).__init__()
        self.__random_level = 0.8

    def __str__(self):
        return "Random bot 0.8"

    def bid(self, player_state, available_locations, current_bid_by_player_id, current_highest_bid):
        if (current_highest_bid >= player_state.money) or (random.random() < self.__random_level):
            return BidResponse(forfeit=True)
        return BidResponse(bid=current_highest_bid + 1)

    def bid_for_cheques(self, player_state, available_cheques):
        if random.random() < self.__random_level:
            return random.choice(player_state.cards)
        return min(player_state.cards)
