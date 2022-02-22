from otree.api import models
from django.db.models import Model, OneToOneField, ForeignKey
from otree.models import Participant
from django.db.models.signals import post_save
from django.dispatch import receiver

author = ""
doc = """
Based on custom-waiting-page-for-mturk by Essi Kujansuu, Philipp Chapkovski, and Nicolas Gruyer/Economics Games.
"""

class AugmentedParticipant(Model):
    Participant = OneToOneField(Participant, on_delete=models.CASCADE, primary_key=True)
    current_wp = models.IntegerField()
    outofthegame = models.BooleanField()


class WPTimeRecord(Model):
    augmented_participant = ForeignKey(AugmentedParticipant, on_delete=models.CASCADE)
    app = models.CharField()
    page_index = models.IntegerField()
    startwp_timer_set = models.BooleanField(default=False)
    startwp_time = models.PositiveIntegerField()
    endwp_time = models.PositiveIntegerField()


class WaitingRoomSlidersTaskRecord(Model):
    augmented_participant = ForeignKey(AugmentedParticipant, on_delete=models.CASCADE)
    app = models.CharField()
    page_index = models.IntegerField()
    sliders_task_set = models.BooleanField(default=False)
    sliders_offsets = models.StringField()
    sliders_curr_values = models.StringField()
    sliders_for_task = models.LongStringField()
    num_centered_sliders = models.IntegerField()
    bonus_per_slider = models.FloatField()


@receiver(post_save, sender=Participant)
def save_participant(sender, instance, **kwargs):
    augmented_participant, created = AugmentedParticipant.objects.get_or_create(Participant=instance)
    augmented_participant.save()

