from abc import ABCMeta, abstractmethod


class PlayerBase(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._my_id = str(self)
        """:type : str"""
        self._current_game_number = None
        """:type : int"""
        self._total_games = None
        """:type : int"""
        self._all_player_ids = None
        """:type : list[str]"""
        self._player_id_to_index = None
        """:type : dict[str, int]"""
        self._my_bidding_index = None
        """:type : int"""

    def __repr__(self):
        return str(self)

    @abstractmethod
    def __str__(self):
        """
        Display name of this player
        """
        pass

    def on_game_start(self, player_state, current_game_number, total_games, all_player_ids):
        """
        Called at the start of a new game
        :param player_state: An immutable copy of the current player state
        :type player_state: utils.PlayerState
        :param current_game_number: The current game number (one based)
        :type current_game_number: int
        :param total_games: The total number of games to be played
        :type total_games: int
        :param all_player_ids: An unsorted list of all the participating players
        :type all_player_ids: list[str]
        """
        self._current_game_number = current_game_number
        self._total_games = total_games
        self._all_player_ids = all_player_ids
        self._player_id_to_index = None
        self._my_bidding_index = None

    #
    # Buying phase
    #

    def on_start_buying_phase(self, player_state):
        """
        Called at the start a the buying phase
        :param player_state: An immutable copy of the current player state, of type PlayerState
        :type player_state: utils.PlayerState
        """
        pass

    def on_start_buying_round(self, player_state, player_id_to_index):
        """
        Called at the start of a new buying round
        :param player_state: An immutable copy of the current player state
        :type player_state: utils.PlayerState
        :param player_id_to_index: A mapping of players IDs to bidding indexes (zero based) for the current round
        :type player_id_to_index: dict[str, int]
        """
        self._player_id_to_index = player_id_to_index
        self._my_bidding_index = player_id_to_index[self._my_id]

    @abstractmethod
    def bid(self, player_state, available_locations, current_bid_by_player_id, current_highest_bid):
        """
        Bid on a location card
        :param player_state: An immutable copy of the current player state
        :type player_state: utils.PlayerState
        :param available_locations: All the available locations, by their values
        :type available_locations: list[int]
        :param current_bid_by_player_id: A mapping between player ID and their current bid. If a player forfeited their
                                        bid is None
        :type current_bid_by_player_id: dict[str, int]
        :param current_highest_bid: The current highest bid across all players
        :type current_highest_bid: int
        :rtype: utils.BidResponse
        """
        pass

    def on_buy(self, player_state, card, price):
        """
        Called when this player gets a new location card, whether by successful bid or by forfeit
        :param player_state: An immutable copy of the current player state
        :type player_state: utils.PlayerState
        :param card: The card value that was bough
        :type card: int
        :param price: The price paid for the card, can be different from the card value
        :type price: int
        """
        pass

    def on_end_buying_round(self, player_state, round_history):
        """
        Called at the end of a buying round
        :param player_state: An immutable copy of the current player state
        :type player_state: utils.PlayerState
        :param round_history: A list of turns, each containing a list of player statuses by index, matching
                            self._player_id_to_index. If a player didn't participate in a round (forfeited before) the
                            corresponding list entry is None. If a player forfeited in a certain round, to bid member
                            for this TurnStatus object is None and the card member has a value
        :type round_history: list[list[utils.TurnStatus]]
        """
        pass

    def on_end_buying_phase(self, player_state):
        """
        Called at the end of the buying phase, when all location cards were handed to players. Now each player has the
        same number of cards
        :param player_state: An immutable copy of the current player state
        :type player_state: utils.PlayerState
        """
        pass

    #
    # Selling phase
    #

    def on_start_selling_phase(self, player_state):
        """
        Called at the start a the selling phase
        :param player_state: An immutable copy of the current player state, of type PlayerState
        :type player_state: utils.PlayerState
        """
        pass

    @abstractmethod
    def bid_for_cheques(self, player_state, available_cheques):
        """
        Choose a location card to bid for one of the available cheques. You must return one of the values in
        player_state.cards
        :param player_state: An immutable copy of the current player state
        :type player_state: utils.PlayerState
        :param available_cheques: All the available cheques, by their values
        :type available_cheques: list[int]
        :rtype: int
        """
        pass

    def on_sell(self, player_state, sell_details_by_player_id):
        """
        Called after every selling round
        :param player_state: An immutable copy of the current player state
        :type player_state: utils.PlayerState
        :param sell_details_by_player_id: A mapping between player ID and a tuple of (location card sold, cheque got)
        :type sell_details_by_player_id: dict[str, (int, int)]
        """
        pass

    def on_end_selling_phase(self, player_state):
        """
        Called at the end of the selling phase, when all cheques were handed to players and all location cards were
        discarded. This is the end of the game.
        :param player_state: An immutable copy of the current player state
        :type player_state: utils.PlayerState
        """
        pass
