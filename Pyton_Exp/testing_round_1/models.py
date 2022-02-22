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
    name_in_url = 'testing_round_1'
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
    q5 = models.StringField(choices=['Partido A', 'Partido B'],
                            label='¿Qué partido ganó la votación?',
                            widget=widgets.RadioSelect)
    q6 = models.IntegerField(min=0, null=True, label='¿Cuántos puntos ganó el votante?')
    q7 = models.IntegerField(min=0, null=True, label='¿Cuántos puntos ganó el partido A?')
    q8 = models.IntegerField(min=0, null=True, label='¿Cuántos puntos ganó el partido B?')

    def q1_error_message(self, value):
        if value != 'Partido B':
            return 'El Partido ganador es el partido B'

    def q2_error_message(self, value):
        if value != 2000:
            return 'el votante ganó 2000 puntos'

    def q3_error_message(self, value):
        if value != 1000:
            return 'el Partido A ganó 1000 puntos'

    def q4_error_message(self, value):
        if value != 2400:
            return 'el Partido B ganó 2400 puntos'

    avanzo1 = models.BooleanField()
    avanzo2 = models.BooleanField()
    avanzo3 = models.BooleanField()
    avanzo4 = models.BooleanField()
    avanzo5 = models.BooleanField()
