from playerbase import PlayerBase
from utils import BidResponse

class NoBananasBot(PlayerBase):

    def __str__(self):
        return "No Bananas Bot"

    def bid(self, player_state, available_locations, current_bid_by_player_id, current_highest_bid):
        pass

    def bid_for_cheques(self, player_state, available_cheques):
        pass

