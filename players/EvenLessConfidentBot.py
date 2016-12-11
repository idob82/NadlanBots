from playerbase import PlayerBase
from utils import BidResponse


class FancyBot(PlayerBase):
    def __str__(self):
        return "Fancy Bot"

    def bid(self, player_state, available_locations, current_bid_by_player_id, current_highest_bid):
        if current_highest_bid >= player_state.money:
            return BidResponse(forfeit=True)
        locations = available_locations
        locations.sort()
        dif = locations[-1] - locations[0]
        if dif <= 3:
            return BidResponse(forfeit=True)
        elif dif >= 10:
            if current_highest_bid <= locations[-1] / 2:
                return BidResponse(bid = current_highest_bid + 1)
        return BidResponse(bid=current_highest_bid + 1)

    def bid_for_cheques(self, player_state, available_cheques):
        cheques = available_cheques
        if cheques is not None:
            cheques.sort()
            if cheques[-1] > 10:
                return max(player_state.cards)
            elif cheques[-1] > 5:
                cards = player_state.cards
                cards.sort()
                return cards[len(cards)/2]
        return min(player_state.cards)

