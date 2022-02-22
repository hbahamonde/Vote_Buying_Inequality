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


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'testing_round_2'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.StringField(choices=['Partido A', 'Partido B'],
                            label='¿Qué partido ganó la votación?',
                            widget=widgets.RadioSelect)
    q2 = models.IntegerField(min=0, null=True, label='¿Cuántos puntos ganó el votante?')
    q3 = models.IntegerField(min=0, null=True, label='¿Cuántos puntos ganó el partido A?')
    q4 = models.IntegerField(min=0, null=True, label='¿Cuántos puntos ganó el partido B?')


    def q1_error_message(self, value):
        if value != 'Partido A':
            return 'El Partido ganador es el partido A'

    def q2_error_message(self, value):
        if value != 2000:
            return 'el votante ganó 2000 puntos'

    def q3_error_message(self, value):
        if value != 3400:
            return 'el Partido A ganó 3400 puntos'

    def q4_error_message(self, value):
        if value != 0:
            return 'el Partido B ganó 0 puntos'

    avanzo6 = models.BooleanField()
    avanzo7 = models.BooleanField()
    avanzo8 = models.BooleanField()
    avanzo9 = models.BooleanField()
