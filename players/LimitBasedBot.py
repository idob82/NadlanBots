import random

from playerbase import PlayerBase
from utils import BidResponse


class LimitBasedBot(PlayerBase):
    def __init__(self):
        super(LimitBasedBot, self).__init__()
        self.__location_limit = 15
        self.__raise_limit = 10
        self.__cheque_upper_limit = 10
        self.__cheque_lower_limit = 3

    def __str__(self):
        return "Limit Based Bot"

    def bid(self, player_state, available_locations, current_bid_by_player_id, current_highest_bid):
        if current_highest_bid >= player_state.money:
            return BidResponse(forfeit=True)

        # Take into account the possible profit
        if (max(available_locations) - min(available_locations)) < self.__location_limit or current_highest_bid >= self.__raise_limit:
            return BidResponse(forfeit=True)

        return BidResponse(bid=current_highest_bid + 1)

    def bid_for_cheques(self, player_state, available_cheques):
        max_cheque = max(available_cheques)
        if max_cheque > self.__cheque_upper_limit:
            return max(player_state.cards)
        if max_cheque < self.__cheque_lower_limit:
            return min(player_state.cards)
        return random.choice(player_state.cards)

