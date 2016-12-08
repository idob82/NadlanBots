import inspect
import os
import random
from collections import defaultdict

import sys

import itertools
import pprint

from NadlanBekatanGame import NadlanBekatanGame


class TournamentRunner(object):

    def __init__(self, player_classes, verbose=True):
        self.player_classes = player_classes
        self.verbose = verbose

    def tournament(self, number_of_players=3, number_of_games=50, number_of_tournaments=100):
        """
        :type number_of_players: int
        :type number_of_games: int
        :type number_of_tournaments: int
        :rtype: dict[str, float]
        """
        global_results = defaultdict(int)
        tournament_count = defaultdict(int)
        matchups = defaultdict(lambda: defaultdict(int))

        if number_of_tournaments is not None:
            tournaments_enum = (random.sample(self.player_classes, number_of_players) for _ in xrange(number_of_tournaments))
        else:
            tournaments_enum = list(itertools.combinations(self.player_classes, number_of_players))

        for tournament_index, chosen_players_classes in enumerate(tournaments_enum):
            # Create new instances of the players classes for each tournament round.
            chosen_players = self.create_player_instances(chosen_players_classes)
            players_ids = [x.get_id() for x in chosen_players]

            tournament_results = self.tournament_for_players(chosen_players, number_of_games)
            if self.verbose:
                print "Finished mini tournament {} for {} players.".format(tournament_index, number_of_players)
                for player_id, score in tournament_results.iteritems():
                    print "Score for player {}:  {}".format(player_id, score)

            for player_id in players_ids:
                global_results[player_id] += tournament_results.get(player_id, 0)
                tournament_count[player_id] += 1

            for player1 in players_ids:
                for player2 in players_ids:
                    # Number of games player 1 won against player 2
                    matchups[player1][player2] += tournament_results.get(player1, 0)

        if self.verbose:
            print "Finished {} tournaments for {} players.".format(number_of_tournaments, number_of_players)
            for player_id, score in global_results.iteritems():
                print "Player: {}. Score: {}. Number of tournaments: {}".format(player_id, score, tournament_count[player_id])
            print

        normalized_results = dict([(player_id, 100. * global_results[player_id] / (tournament_count[player_id] * number_of_games))
                                   for player_id in global_results.iterkeys()])

        return normalized_results, matchups

    @staticmethod
    def tournament_for_players(players, number_of_games=100):
        """
        :type players: list[playerbase.PlayerBase]
        :type number_of_games: int
        :rtype: dict[str, float]
        """
        all_player_ids = [x.get_id() for x in players]
        tournament_results = dict([(player_id, 0) for player_id in all_player_ids])

        # Run game rounds rounds
        for game_number in xrange(1, number_of_games + 1):
            game_server = NadlanBekatanGame(players, current_game_number=game_number, total_games=number_of_games)
            winners = game_server.run_game()
            for winner_id in winners:
                if len(winners) == 1:
                    win_addition = 1
                else:
                    win_addition = 1.0 / len(winners)
                assert winner_id in tournament_results
                tournament_results[winner_id] += win_addition
        return tournament_results

    @staticmethod
    def create_player_instances(player_classes):
        """
        :type player_classes: list[type]
        :rtype: list[playerbase.PlayerBase]
        """
        result = [x() for x in player_classes]
        random.shuffle(result)
        return result


def get_all_player_classes():
    """
    :rtype: list[type]
    """
    all_players = []
    for module in os.listdir(os.path.join(os.path.dirname(__file__), "players")):
        if module == "__init__.py" or module[-3:] != ".py":
            continue
        player_module_name = "players." + module[:-3]
        all_players.append(player_module_name)
        __import__(player_module_name, locals(), globals())

    player_classes = [get_primary_class_in_module(module_name) for module_name in all_players]
    player_classes = [x for x in player_classes if not inspect.isabstract(x)]
    return player_classes


def get_primary_class_in_module(module_name):
    """
    :type module_name: str
    :rtype: type
    """
    module = sys.modules[module_name]
    all_objects = inspect.getmembers(module,
                                     lambda member: inspect.isclass(member) and member.__module__ == module_name)
    assert len(all_objects) == 1
    return all_objects[0][1]


def main():
    player_classes = get_all_player_classes()

    print "Starting tournament with {} player types".format(len(player_classes))
    tournament_runner = TournamentRunner(player_classes)
    tournament_results, matchups = tournament_runner.tournament()
    print "Results:"
    for (player_id, win_count) in tournament_results.iteritems():
        print "'{}' won {:2.1f}% of its games".format(player_id, win_count)
    print "Match-ups (how many times a bot won against each another bot"
    for player_id in matchups.keys():
        print "Bot \"{}\" matches: {}".format(player_id, dict(matchups[player_id]))

if __name__ == "__main__":
    sys.exit(main())
