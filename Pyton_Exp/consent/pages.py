from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Consent(Page):
    form_fields = ['consent']
    form_model = 'player'

    def before_next_page(self):
        self.participant.vars['consent'] = self.player.consent


class NoConsent(Page):
    def is_displayed(self):
        return self.player.consent == False


page_sequence = [
    Consent,
    NoConsent
]
