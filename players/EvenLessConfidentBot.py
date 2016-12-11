from playerbase import PlayerBase
from utils import BidResponse


class AlwaysRaiseBot(PlayerBase):
    def __str__(self):
        return "Even Less Confident Bot"

    def bid(self, player_state, available_locations, current_bid_by_player_id, current_highest_bid):
        return BidResponse(forfeit=True)

    def bid_for_cheques(self, player_state, available_cheques):
        cards = player_state.cards
        cards.sort()

        return cards[len(cards) / 2]
