from playerbase import PlayerBase
from utils import BidResponse
import random

class NoBananasBot(PlayerBase):

    other_cards = []
    cards_remaining = range(1, 31)
    difference = 4
    cheque_difference = 2

    def __str__(self):
        return "No Bananas Bot"

    def bid(self, player_state, available_locations, current_bid_by_player_id, current_highest_bid):
        if max(available_locations) - min(available_locations) <= self.difference:
            return BidResponse(forfeit=True)
        if player_state.money <= current_highest_bid:
            return BidResponse(forfeit=True)
        if self.investment_value(max(available_locations)) < current_highest_bid:
            return BidResponse(forfeit=True)
        return BidResponse(bid=current_highest_bid+1)

    def investment_value(self, card):
        return card/2.833

    def return_value(self, card):
        return card/2.0

    def card_to_invest(self, cards, cheque):
        cards = filter(lambda x: self.return_value(x) > cheque, cards)
        if cards:
            return sorted(cards)[0]

    def bid_for_cheques(self, player_state, available_cheques):
        if max(available_cheques) - min(available_cheques) <= self.cheque_difference:
            return min(player_state.cards)
        if max(available_cheques) + self.cheque_difference >= max(player_state.cards) / 2:
            return max(player_state.cards)
        for c in sorted(available_cheques)[::-1]:
            card = self.card_to_invest(player_state.cards, c)
            if card:
                return card
        return min(player_state.cards)
