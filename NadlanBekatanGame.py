import copy
import inspect
import os
import random
import sys
from collections import defaultdict

from utils import PlayerState, TurnStatus

CARDS_TO_REMOVE = defaultdict(int)
CARDS_TO_REMOVE[4] = 2

STARTING_AMOUNT = {3: 28, 4: 21, 5: 16, 6: 14}


class NadlanBekatanGame(object):
    def __init__(self, players, current_game_number=1, total_games=1, verbose=False):
        """
        :type players: list[playerbase.PlayerBase]
        :type current_game_number: int
        :type total_games: int
        :type verbose: bool
        """
        self.__players = players
        if len(players) not in STARTING_AMOUNT:
            raise Exception("Illegal number of players: {}".format(len(players)))
        self.__current_game_number = current_game_number
        self.__total_games = total_games
        self.__verbose = verbose

        self.__all_player_ids = set([x.get_id() for x in players])
        if len(self.__all_player_ids) != len(players):
            raise Exception("Found two players with the same ID. All players: {}".format(players))
        self.__number_of_players = len(players)
        self.__player_states = dict([(player_id, PlayerState()) for player_id in self.__all_player_ids])
        """:type : dict[str, utils.PlayerState]"""

    def run_game(self):
        # Prepare game assets
        locations = range(1, 31)
        random.shuffle(locations)
        cheques = [0, 0] + range(2, 16) * 2
        random.shuffle(cheques)

        # Remove the needed amount of locations and cheques
        for _ in xrange(CARDS_TO_REMOVE[self.__number_of_players]):
            cheques.pop()
            locations.pop()
        assert len(locations) == len(cheques)
        assert len(locations) % self.__number_of_players == 0

        # Distribute money!
        for state in self.__player_states.itervalues():
            state.money = STARTING_AMOUNT[self.__number_of_players]

        for player in self.__players:
            player.on_game_start(self.get_read_only_state(player),
                                 self.__current_game_number,
                                 self.__total_games,
                                 self.create_read_only_copy(self.__all_player_ids))

        # Phase 1 - buying

        for player in self.__players:
            player.on_start_buying_phase(self.get_read_only_state(player))

        # Assign initial positions randomly
        players_order = [x for x in self.__players]
        random.shuffle(players_order)

        # Play rounds until we run out of location cards
        while len(locations) > 0:
            winner_index = self.buying_round(locations, players_order)
            assert winner_index >= 0
            assert winner_index < len(players_order)
            players_order = self.rotate_list(players_order, winner_index)

        for player in self.__players:
            player.on_end_buying_phase(self.get_read_only_state(player))

        if self.__verbose:
            print "Players state after buying phase: ", self.__player_states

        # Phase 2 - selling

        for player in self.__players:
            player.on_start_selling_phase(self.get_read_only_state(player))

        while len(cheques) > 0:
            self.selling_round(cheques)

        for player in self.__players:
            player.on_end_selling_phase(self.get_read_only_state(player))

        if self.__verbose:
            print "Players state after selling phase: ", self.__player_states

        # Calculate winners
        total_assets = dict([(player_id, state.money + sum(state.cheques)) for (player_id, state) in
                             self.__player_states.iteritems()])
        winners = self.keys_with_max_value(total_assets)
        if len(winners) > 1:
            # On total money draw, the player with more cash wins.
            winners_money = dict([(player_id, self.__player_states[player_id].money) for player_id in winners])
            winners = self.keys_with_max_value(winners_money)
        return winners

    def get_read_only_state(self, player):
        return self.create_read_only_copy(self.__player_states[player.get_id()])

    def buying_round(self, locations, players_order):
        """
        :type locations: list[int]
        :type players_order: list[playerbase.PlayerBase]
        """
        locations_chosen = []
        for i in range(self.__number_of_players):
            locations_chosen.append(locations.pop())
        locations_chosen.sort()

        player_ids_order = [x.get_id() for x in players_order]
        if self.__verbose:
            print "START OF BUYING ROUND. Players order {}. Locations: {}".format(player_ids_order, locations_chosen)
        for player in self.__players:
            player.on_start_buying_round(self.get_read_only_state(player), self.create_read_only_copy(player_ids_order))

        round_history = []
        active_players_by_order = [x for x in players_order]
        current_bid_by_player_id = dict([(player_id, 0) for player_id in self.__all_player_ids])

        while len(locations_chosen) > 0:
            turn_stats = [None] * self.__number_of_players
            for player_index in xrange(self.__number_of_players):
                current_player = active_players_by_order[player_index]
                if current_player is None:
                    continue

                current_player_id = current_player.get_id()

                if len(locations_chosen) == 1:
                    # Give the last card to the last active player
                    self.handle_last_location(active_players_by_order, current_bid_by_player_id,
                                                         current_player, current_player_id, locations_chosen,
                                                         player_index, turn_stats)
                    winner_index = player_index
                    break

                assert len(locations_chosen) > 1  # Should not have active players with no more cards

                self._handle_player_bid(active_players_by_order, current_bid_by_player_id, current_player,
                                        current_player_id, locations_chosen, player_index, turn_stats)
            round_history.append(turn_stats)

        assert all([x is None for x in active_players_by_order])

        if self.__verbose:
            print "END OF BUYING ROUND. History: {}".format(round_history)
        for player in self.__players:
            player.on_end_buying_round(self.get_read_only_state(player), round_history)

        return winner_index

    def handle_last_location(self, active_players_by_order, current_bid_by_player_id, current_player, current_player_id,
                             locations_chosen, player_index, turn_stats):
        # Only one card left, meaning only one player left, and they pay the full price and get the
        # highest card
        assert len([x for x in active_players_by_order if x is not None]) == 1
        highest_location = locations_chosen.pop()
        self.__player_states[current_player_id].money -= current_bid_by_player_id[current_player_id]
        self.__player_states[current_player_id].cards.append(highest_location)
        active_players_by_order[player_index] = None
        turn_stats[player_index] = TurnStatus(current_player_id, current_bid_by_player_id[current_player_id], highest_location)
        current_player.on_buy(self.get_read_only_state(current_player),
                              highest_location,
                              current_bid_by_player_id[current_player_id])

    def _handle_player_bid(self, active_players_by_order, current_bid_by_player_id, current_player, current_player_id,
                           locations_chosen, player_index, turn_stats):
        bid_response = current_player.bid(self.get_read_only_state(current_player),
                                          self.create_read_only_copy(locations_chosen),
                                          self.create_read_only_copy(current_bid_by_player_id),
                                          max(current_bid_by_player_id.itervalues()))
        if bid_response.forfeit:
            # The player forfeits, give them the lowest location card and kick them out of this round
            smallest_location = locations_chosen.pop()
            price = current_bid_by_player_id[current_player_id] / 2

            self.__player_states[current_player_id].money -= price
            self.__player_states[current_player_id].cards.append(smallest_location)

            active_players_by_order[player_index] = None
            current_bid_by_player_id[current_player_id] = None
            turn_stats[player_index] = TurnStatus(current_player_id, price, smallest_location)

            current_player.on_buy(self.get_read_only_state(current_player),
                                  smallest_location,
                                  price)
        else:
            # Make sure they can buy it
            if bid_response.value > self.__player_states[current_player_id].money:
                raise Exception("Player attempted to bid more money than they have! Bid: {}, have: {}"
                                .format(bid_response.value, self.__player_states[current_player_id].money))
            if bid_response.value <= max(current_bid_by_player_id.itervalues()):
                raise Exception("Player attempted to bid less than the current high bid! Bid: {}, currently: {}"
                                .format(bid_response.value, max(current_bid_by_player_id.itervalues())))

            current_bid_by_player_id[current_player_id] = bid_response.value
            turn_stats[player_index] = TurnStatus(current_player_id, bid_response.value, None)

    def selling_round(self, cheques):
        """
        :type cheques: list[int]
        """
        cheques_chosen = []
        for i in range(self.__number_of_players):
            cheques_chosen.append(cheques.pop())
            cheques_chosen.sort()

        if self.__verbose:
            print "START OF SELLING ROUND. Cheques: {}".format(cheques_chosen)

        player_locations = []
        for current_player in self.__players:
            location = current_player.bid_for_cheques(self.get_read_only_state(current_player),
                                                      self.create_read_only_copy(cheques_chosen))
            if location not in self.__player_states[current_player.get_id()].cards:
                raise Exception("Player attempted to sell a location card they don't have! Location: {}"
                                .format(location))
            player_locations.append((current_player.get_id(), location))

        player_locations.sort(key=lambda (_, location_card): location_card)

        sell_details_by_player_id = {}
        for index, (player_id, location) in enumerate(player_locations):
            sell_details_by_player_id[player_id] = (location, cheques_chosen[index])
            self.__player_states[player_id].cards.remove(location)
            self.__player_states[player_id].cheques.append(cheques_chosen[index])

        for current_player in self.__players:
            current_player.on_sell(self.get_read_only_state(current_player),
                                   self.create_read_only_copy(sell_details_by_player_id))

        if self.__verbose:
            print "END OF SELLING ROUND. Locations used: {}" \
                .format([location for (_, location) in player_locations])

    @staticmethod
    def rotate_list(elements, new_head_index):
        return elements[new_head_index:] + elements[:new_head_index]

    @staticmethod
    def keys_with_max_value(dictionary):
        max_value = max(dictionary.itervalues())
        return [key for (key, value) in dictionary.iteritems() if value == max_value]

    @staticmethod
    def create_read_only_copy(value):
        """
        Helper function to create a read-only copy of complex objects that we pass to the players, because we
        don't trust them not to manipulate our internal state :)
        """
        return copy.deepcopy(value)

