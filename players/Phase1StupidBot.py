from playerbase import PlayerBase
from utils import BidResponse


class Phase1StupidBot(PlayerBase):
    def __str__(self):
        return "Stupid bot"

    def bid(self, player_state, available_locations, current_bid_by_player_id, current_highest_bid):
        if current_highest_bid >= player_state.money:
            return BidResponse(forfeit=True)
        return BidResponse(bid=current_highest_bid + 1)

    def bid_for_cheques(self, player_state, available_cheques):
        sorted_cards = sorted(player_state.cards)
        return sorted_cards[0]
