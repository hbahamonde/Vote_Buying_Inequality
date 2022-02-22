from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class PreIntro(Page):
    #timeout_seconds = 90

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanzo6 = True


class Intro(Page):
    #timeout_seconds = 45

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanzo7 = True


class Ensayo1(Page):
    #timeout_seconds = 120
    form_fields = ['q1', 'q2', 'q3', 'q4']
    form_model = 'player'

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanzo8 = True


class Feedback(Page):
    timeout_seconds = 15


class FinEnsayo(Page):
    #timeout_seconds = 30

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanzo9 = True


page_sequence = [PreIntro, Intro, Ensayo1, Feedback, FinEnsayo]
