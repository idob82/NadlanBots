from playerbase import PlayerBase
from utils import BidResponse
import random

class NotImplemnted(PlayerBase):
    def __str__(self):
        return "Not Implemented Bot"

    def bid(self, player_state, available_locations, current_bid_by_player_id, current_highest_bid):
        if current_highest_bid >= player_state.money or \
                (len(player_state.cards) > 0 and max(available_locations) < sum(player_state.cards) / len(player_state.cards)) or \
                (len(player_state.cards) > 0 and min(available_locations) > sum(player_state.cards) / len(player_state.cards)):
            return BidResponse(forfeit=True)
        return BidResponse(bid=current_highest_bid + 1)

    def bid_for_cheques(self, player_state, available_cheques):
        sorted_cheques = sorted(available_cheques)

        max_cheque = max(available_cheques)
        if max_cheque > 10:
            return self._best_match(player_state.cards, sorted_cheques[2])
        if max_cheque < 3:
            return self._best_match(player_state.cards, sorted_cheques[0])
        else:
            return self._best_match(player_state.cards, sorted_cheques[1])

    def _best_match(self, cards, cheque):
        dists = []
        for card in cards:
            delta = abs(card - cheque *2)
            dists.append((card, delta))

        dists.sort(key=lambda x: x[1], reverse=False)
        return dists[0][0]

    def on_end_buying_phase(self, player_state):
        pass
        # print 'Our Bot:', player_state.cards
        # s = raw_input()

    def on_end_buying_round(self, player_state, round_history):
        pass
        # for i in round_history:
        #    print i
        #s = raw_input()