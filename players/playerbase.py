from abc import ABCMeta, abstractmethod


class PlayerBase(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.money = 0
        self.cards = []

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return str(self)
