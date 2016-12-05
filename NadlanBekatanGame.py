import inspect
import os
import random
import sys
from collections import defaultdict

CARD_TAKEN = -1
CARDS_TO_REMOVE = defaultdict(int)
CARDS_TO_REMOVE[3] = 6
STARTING_AMOUNT = defaultdict(int)
STARTING_AMOUNT[3] = 24
STARTING_AMOUNT[4] = 21


class NadlanBekatanGame(object):
    def run_game(self, bots, verbose=False):
        number_of_bots = len(bots)
        locations = range(1, 31)
        cheques = [0, 0] + range(2, 16) + range(2, 16)
        # Remove the needed amount random locations and cheques
        for _ in range(CARDS_TO_REMOVE[number_of_bots]):
            index = random.randint(0, len(locations) - 1)
            cheques.pop(index)
            locations.pop(index)

        # Phase 1:
        # Bidding wars
        # Choose locations for bid
        bots_money = [STARTING_AMOUNT[number_of_bots]] * number_of_bots
        bots_cards = [[] for i in range(number_of_bots)]
        [bot.init(STARTING_AMOUNT[number_of_bots]) for bot in bots]

        starting_bot = 0
        while len(locations) > 0:
            starting_bot = self.bidding_round(starting_bot, bots_cards, bots_money, locations, bots, verbose)

        if verbose:
            print "Bots money after bidding stage:", bots_money
            print "Cards", bots_cards

        while len(cheques) > 0:
            self.buying_round(bots_money, bots_cards, bots, cheques, verbose)

        winner_amount = max(bots_money)
        winners = [i for i in range(len(bots_money)) if bots_money[i] == winner_amount]

        if verbose:
            print "Amount of money left:", bots_money
        return winners

    def bidding_round(self, starting_bot, bots_cards, bots_money, locations, bots, verbose=False):
        number_of_bots = len(bots)
        locations_chosen = []
        for i in range(number_of_bots):
            index = random.randint(0, len(locations) - 1)
            locations_chosen.append(locations[index])
            locations.pop(index)
        locations_chosen.sort()
        if verbose:
            print "START OF BIDDING ROUND. starting bot {}. Money: {}. locations: {}".format(starting_bot,
                                                                                             bots_money,
                                                                                             locations_chosen)
        bots_in_play = range(number_of_bots)
        bot_in_list_index = starting_bot
        current_bid = 0
        last_buyer = -1
        bids = {}
        for i in range(number_of_bots):
            bids[i] = [0]

        while len(locations_chosen) > 0:
            bot_in_list_index %= len(bots_in_play)
            current_bot_index = bots_in_play[bot_in_list_index]
            current_bot = bots[current_bot_index]

            bid_response = current_bot.bid(locations_chosen, bids, current_bid)

            if bid_response.buy or not self.validate_bid_response(bid_response.value, bots_money[current_bot_index],
                                                                  current_bid):
                bot_bid = bids[current_bot_index][-1]
                card_to_take = locations_chosen.pop(0)
                if len(locations_chosen) == 0:
                    price = bot_bid
                else:
                    price = bot_bid / 2
                bots_money[current_bot_index] -= price
                bots_cards[current_bot_index].append(card_to_take)

                current_bot.buy(card_to_take, price)

                # To allow full data - append None
                bids[current_bot_index].append(CARD_TAKEN)
                bots_in_play.pop(bot_in_list_index)
                last_buyer = current_bot_index
            else:
                # bid_response is valid, and raises the bid
                bids[current_bot_index].append(bid_response.value)
                current_bid = bid_response.value
                bot_in_list_index += 1
        for bot in bots:
            bot.end_bidding_round()
        if verbose:
            print "END OF ROUND. bids: {}".format(bids)
        return last_buyer

    @staticmethod
    def buying_round(bots_money, bots_cards, bots, cheques, verbose=False):
        number_of_bots = len(bots)
        cheques_chosen = []
        for _ in range(number_of_bots):
            index = random.randint(0, len(cheques) - 1)
            cheques_chosen.append(cheques[index])
            cheques.pop(index)
        cheques_chosen.sort()
        if verbose:
            print "START OF BUYING ROUND. cheques: {}. available cards: {}".format(cheques_chosen, bots_cards)

        location_bid_mapping = {}

        for index in range(len(bots)):
            bot = bots[index]
            location = bot.bid_for_cheques(cheques_chosen)
            if location not in bots_cards[index]:
                print "Invalid location chosen. Choosing first not in use"
                location = bots_cards[index][0]
            bots_cards[index].remove(location)
            location_bid_mapping[location] = index

        sorted_locations = sorted(location_bid_mapping.keys())
        for index in range(len(sorted_locations)):
            location = sorted_locations[index]
            bot_index = location_bid_mapping[location]
            bots_money[bot_index] += cheques_chosen[index]
            bots[bot_index].buy_cheque(location, cheques_chosen[index], location_bid_mapping)

        for bot in bots:
            bot.end_buying_round()
        if verbose:
            print "END OF ROUND. Locations used: {}".format(sorted_locations)

    @staticmethod
    def validate_bid_response(value, bot_money, current_bid):
        return current_bid < value <= bot_money


game_server = NadlanBekatanGame()


def tournament(bots, number_of_rounds=100):
    tournament_results = [0] * len(bots)
    # Do 100 rounds
    for i in range(number_of_rounds):
        winners = game_server.run_game(bots)
        for w in winners:
            tournament_results[w] += 1.0 / len(winners)
    return tournament_results


def get_all_player_classes():
    all_players = []
    for module in os.listdir(os.path.join(os.path.dirname(__file__), "players")):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        player_module_name = "players." + module[:-3]
        all_players.append(player_module_name)
        __import__(player_module_name, locals(), globals())

    player_classes = [get_primary_class_in_module(module_name) for module_name in all_players]
    player_classes = [x for x in player_classes if not inspect.isabstract(x)]
    return player_classes


def get_primary_class_in_module(module_name):
    module = sys.modules[module_name]
    all_objects = inspect.getmembers(module,
                                     lambda member: inspect.isclass(member) and member.__module__ == module_name)
    assert len(all_objects) == 1
    return all_objects[0][1]


def create_player_instances(player_classes):
    return [x() for x in player_classes]


def main():
    player_classes = get_all_player_classes()
    players = create_player_instances(player_classes)
    winner = game_server.run_game(players, verbose=True)

    print "Winners for first game are:", winner

    print "Starting tournament", players
    tournament_results = tournament(players)
    for i in range(len(players)):
        print players[i], "won", tournament_results[i], "rounds"

    players = create_player_instances(player_classes)

    print "Starting tournament", players
    tournament_results = tournament(players)
    for i in range(len(players)):
        print players[i], "won", tournament_results[i], "rounds"


if __name__ == "__main__":
    sys.exit(main())
