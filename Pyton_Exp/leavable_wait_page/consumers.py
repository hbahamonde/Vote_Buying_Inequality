from .models import AugmentedParticipant, WaitingRoomSlidersTaskRecord
from otree.models import Participant
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from importlib import import_module
import json


class LeavableWaitPageConsumer(WebsocketConsumer):

    def _get_models_module(self, app_name):
        module_name = '{}.models'.format(app_name)
        return import_module(module_name)

    def update_state(self, app_name, group_pk, index_in_pages):
        participants_on_wait_page = self._get_models_module(app_name).Player.objects.filter(
            group__pk=group_pk,
            participant__augmentedparticipant__current_wp=index_in_pages,
        )
        num_waiting_participants = len(participants_on_wait_page)
        players_per_group = self._get_models_module(app_name).Constants.players_per_group
        num_missing_participants = players_per_group - num_waiting_participants

        payload = {
            "num_waiting_participants": num_waiting_participants,
            "num_missing_participants": num_missing_participants,
        }

        async_to_sync(self.channel_layer.group_send)(
            'group_{}_{}'.format(app_name, group_pk),
            {
                "type": "group_forward",
                "text": json.dumps(payload)
            }
        )

    def connect(self):
        participant_code = self.scope['url_route']['kwargs']['participant_code']
        app_name = self.scope['url_route']['kwargs']['app_name']
        group_pk = self.scope['url_route']['kwargs']['group_pk']
        index_in_pages = self.scope['url_route']['kwargs']['index_in_pages']


        try:
            mturker = AugmentedParticipant.objects.get(Participant__code=participant_code)
        except ObjectDoesNotExist:
            return None

        mturker.current_wp = index_in_pages
        mturker.save()

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            'group_{}_{}'.format(app_name, group_pk),
            self.channel_name
        )
        self.update_state(app_name, group_pk, index_in_pages)

    def receive(self, text_data=None, bytes_data=None):

        participant_code = self.scope['url_route']['kwargs']['participant_code']
        app_name = self.scope['url_route']['kwargs']['app_name']
        index_in_pages = self.scope['url_route']['kwargs']['index_in_pages']

        jsonmessage = json.loads(text_data)

        sliders_curr_values = jsonmessage.get('sliders_curr_values')
        num_centered_sliders = jsonmessage.get('num_centered_sliders')

        if sliders_curr_values:
            with transaction.atomic():
                try:
                    mturker = AugmentedParticipant.objects.select_for_update().get(Participant__code=participant_code)
                    wpslidersrecord = WaitingRoomSlidersTaskRecord.objects.get(augmented_participant_id=mturker,
                                                       page_index=index_in_pages,
                                                       app=app_name)
                except ObjectDoesNotExist:
                    return None

                wpslidersrecord.sliders_curr_values = json.dumps(sliders_curr_values)
                wpslidersrecord.num_centered_sliders = num_centered_sliders
                wpslidersrecord.save()


    # Connected to websocket.disconnect
    def disconnect(self, close_code):
        participant_code = self.scope['url_route']['kwargs']['participant_code']
        app_name = self.scope['url_route']['kwargs']['app_name']
        group_pk = self.scope['url_route']['kwargs']['group_pk']
        index_in_pages = self.scope['url_route']['kwargs']['index_in_pages']
        try:
            mturker = AugmentedParticipant.objects.get(Participant__code=participant_code)
            wpslidersrecord = WaitingRoomSlidersTaskRecord.objects.get(augmented_participant_id=mturker,
                                                                       page_index=index_in_pages,
                                                                       app=app_name)
            curparticipant = Participant.objects.get(code__exact=participant_code)
        except ObjectDoesNotExist:
            return None

        mturker.current_wp = None
        mturker.save()
        curparticipant.vars['num_centered_sliders'] = wpslidersrecord.num_centered_sliders
        curparticipant.vars['waiting_room_task_bonus'] = curparticipant.vars[
                                                      'num_centered_sliders'] * wpslidersrecord.bonus_per_slider
        curparticipant.save()

        async_to_sync(self.channel_layer.group_discard)(
            'group_{}_{}'.format(app_name, group_pk),
            self.channel_name
        )

        self.update_state(app_name, group_pk, index_in_pages)

    # receive from room then forward to everyone in group
    def group_forward(self, event):
        self.send(text_data=event['text'])

    def participant_forward(self, event):
        self.send(text_data=event['text'])
