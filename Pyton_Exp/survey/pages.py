from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from . import models


class Survey(Page):
    form_model = models.Player
    form_fields = ['q1', 'q2', 'q3']


class Survey2(Page):
    form_model = models.Player
    form_fields = ['q4', 'q5']


class Survey3(Page):
    form_model = models.Player
    form_fields = ['q6', 'q7', 'q8', 'q9', 'q10']


page_sequence = [
    Survey, Survey2, Survey3
]
