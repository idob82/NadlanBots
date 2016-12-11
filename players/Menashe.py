import random

from playerbase import PlayerBase
from utils import BidResponse

class MenasheBot(PlayerBase):

    def __init__(self):
        super(MenasheBot, self).__init__()

    def __str__(self):
        return "The one to rule them all"

    def bid(self, player_state, available_locations, current_bid_by_player_id, current_highest_bid):


        if len(available_locations) == 3 and available_locations[0] >= 14:
            return BidResponse(forfeit=True)

        if current_highest_bid <= available_locations[-1] - 15:
            if current_highest_bid >= player_state.money:
                return BidResponse(forfeit=True)
            return BidResponse(bid=current_highest_bid + 1)

        return BidResponse(forfeit=True)


    def bid_for_cheques(self, player_state, available_cheques):
        return min(player_state.cards)