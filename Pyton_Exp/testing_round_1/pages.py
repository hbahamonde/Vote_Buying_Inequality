from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class PreIntro(Page):
    #timeout_seconds = 90

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanzo1 = True


class Intro(Page):
    #timeout_seconds = 45

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanzo2 = True


class Feedback(Page):
    timeout_seconds = 15


class Ensayo1(Page):
    #timeout_seconds = 120
    form_fields = ['q1', 'q2', 'q3', 'q4']
    form_model = 'player'

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanzo3 = True


class Ensayo2(Page):
    #timeout_seconds = 120
    form_fields = ['q5', 'q6', 'q7', 'q8']
    form_model = 'player'

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanzo4 = True


class FinEnsayo(Page):
    #timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanzo5 = True


page_sequence = [PreIntro, Intro, Ensayo1, Feedback, FinEnsayo]
