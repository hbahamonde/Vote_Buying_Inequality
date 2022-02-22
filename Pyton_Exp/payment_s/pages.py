from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):

    def vars_for_template(self):
        participant = self.participant
        return {
            'redemption_code': participant.label or participant.code,
            'pago2': participant.vars['votos_s'],
            'show_up': Constants.show_up,
            'pago3': participant.payoff_plus_participation_fee()
        }


class EndofSurvey(Page):
    def vars_for_template(self):
        participant = self.participant
        return {
            'redemption_code': participant.label or participant.code,
            'pago2': participant.vars['votos_s'],
            'show_up': Constants.show_up,
            'pago3': participant.payoff_plus_participation_fee()
        }


page_sequence = [Results, EndofSurvey]
