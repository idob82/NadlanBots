import random
import math

from playerbase import PlayerBase
from utils import BidResponse


class LimitBasedBot(PlayerBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.__location_limit = 15
        self.__raise_limit = 10
        self.__cheque_upper_limit = 10
        self.__cheque_lower_limit = 3


    def __str__(self):
        """ MUST """
        return "Experimental"

    def bid(self, player_state, available_locations, current_bid_by_player_id, current_highest_bid):
        """ MUST """
        


        if  current_highest_bid >= player_state.money:
            return BidResponse(forfeit=True)
        if max(available_locations) - min(available_locations) <=4:
            return BidResponse(True)
        elif max(available_locations) - min(available_locations) > 20:
            if current_highest_bid < 13:
                return BidResponse(bid=current_highest_bid + 1)
        return BidResponse(True)


    def bid_for_cheques(self, player_state, available_cheques):
        """ MUST """
        if max(available_cheques) - min(available_cheques) <=4:
            return min(player_state.cards)
        elif max(available_cheques) - min(available_cheques) > 20:
            return max(player_state.cards)
        return  random.choice(player_state.cards)