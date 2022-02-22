from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from leavable_wait_page.pages import SkippablePage, LeavableWaitPage


class GroupParticipants(LeavableWaitPage):
    """This is a wait page that allows players to quit waiting after 10 seconds."""
    allow_leaving_after = 60 * Constants.max_min_in_waiting_room


class ContinueToExperiment(SkippablePage):
    def is_displayed(self):
        if self.participant.vars.get("waiting_room_task_bonus"):
            return True
        else:
            return False


class Dropouts(Page):
    """This page is only shown to those who left the wait page."""
    def is_displayed(self) -> bool:
        return self.player.participant.vars.get('go_to_the_end', False)

    def vars_for_template(self):
        return {"waiting_room_task_bonus": self.participant.vars["waiting_room_task_bonus"]}


page_sequence = [
    GroupParticipants,
    ContinueToExperiment,
    Dropouts
]