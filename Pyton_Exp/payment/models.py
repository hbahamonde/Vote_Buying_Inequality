from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Mauricio López Tapia'

doc = """
Payment calculation
"""


class Constants(BaseConstants):
    name_in_url = 'payment'
    players_per_group = None
    num_rounds = 1
    show_up = 2000


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.payoff = 0


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
