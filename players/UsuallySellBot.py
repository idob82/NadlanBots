from players_prototypes.RandomBotPrototype import RandomBotPrototype


class UsuallySellBot(RandomBotPrototype):
    def __init__(self):
        super(UsuallySellBot, self).__init__(0.4)

    def __str__(self):
        return "Usually Sell Bot"
