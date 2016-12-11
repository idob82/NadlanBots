from playerbase import PlayerBase
from utils import BidResponse
import math

class TestBot(PlayerBase):
	def __init__(self):
		super(TestBot, self).__init__()
		self.__location_limit = 15
		self.__max_raise_limit = 0
		self.__med_raise_limit = 0
		self.__min_raise_limit = 0
		self.__max_take_difference = 5

	def __str__(self):
		return "Test Bot"

	def on_start_buying_phase(self, player_state):
		self.__max_raise_limit = player_state.money / 10
		self.__med_raise_limit = player_state.money / 15
		self.__min_raise_limit = player_state.money / 20

	def bid(self, player_state, available_locations, current_bid_by_player_id, current_highest_bid):
		highest_card = max(available_locations)
		lowest_card = min(available_locations)
		if highest_card - lowest_card <= self.__max_take_difference:
			return BidResponse(forfeit = True)
		if highest_card > 20:
			#pay up to max limit
			if current_highest_bid < self.__max_raise_limit:
				return BidResponse(bid = current_highest_bid + 1)
			return BidResponse(forfeit = True)
		if highest_card > 10:
			#pay up to medium limit
			if current_highest_bid < self.__med_raise_limit:
				return BidResponse(bid = current_highest_bid + 1)
			return BidResponse(forfeit = True)
		#pay up to medium limit
		if current_highest_bid < self.__min_raise_limit:
			return BidResponse(bid = current_highest_bid + 1)
		return BidResponse(forfeit = True)

	def bid_for_cheques(self, player_state, available_cheques):
		highest_cheque = max(available_cheques)
		lowest_cheque = min(available_cheques)
		if highest_cheque > 10:
			return max(player_state.cards)
		if highest_cheque > 5:
			index = int(len(player_state.cards) / 2)
			cards = player_state.cards
			cards.sort()
			return cards[index]
		return min(player_state.cards)