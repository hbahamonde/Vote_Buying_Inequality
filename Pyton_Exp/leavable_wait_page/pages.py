from otree.api import (models, Currency as c)
import time
from django.http import HttpResponseRedirect
from otree.models import Participant
from . import models
from ._builtin import Page, WaitPage

import json


# Sliders task params
num_sliders = 48
slider_columns = 3
sliders_max = 100
sliders_min = 0
middle_value = 50


# For creating the sliders task
def _chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def create_sliders_task(num_sliders, slider_columns, value_min, value_middle, value_max, offsets=None, current_values=None):
    import random
    if not offsets:
        offsets = [random.randint(0, 10) for _ in range(num_sliders // slider_columns)]
    if not current_values:
        values = [v for v in range(value_min, middle_value)] + [v for v in range(value_middle+1, value_max+1)]
        current_values = [random.choice(values) for _ in range(num_sliders)]
    sliders_for_task = list(zip(_chunks(current_values, slider_columns), offsets))
    return offsets, current_values, sliders_for_task



class DecorateIsDisplayMixin(object):
    def __init__(self):
        super(DecorateIsDisplayMixin, self).__init__()

        # We need to edit is_displayed() method dynamically, when creating an instance, since custom use is that it is
        # overriden in the last child
        def decorate_is_displayed(func):
            def decorated_is_display(*args, **kwargs):
                app_name = self.player._meta.app_label
                round_number = self.player.round_number
                exiter = self.player.participant.vars.get('go_to_the_end', False) or self.player.participant.vars.get(
                    'skip_the_end_of_app_{}'.format(app_name), False) or self.player.participant.vars.get(
                    'skip_the_end_of_app_{}_round_{}'.format(app_name, round_number), False)

                game_condition = func(*args, **kwargs)
                # we need to first run them both separately to make sure that both conditions are executed

                return game_condition and not exiter

            return decorated_is_display

        setattr(self, "is_displayed", decorate_is_displayed(getattr(self, "is_displayed")))


class SkippablePage(DecorateIsDisplayMixin, Page):
    pass


class LeavableWaitPage(WaitPage):
    # Only for the first, grouping wait page of the app
    template_name = 'leavable_wait_page/LeavableWaitPage.html'

    # In case a player waits more than allow_leaving_after (expressed in seconds), he will be offered the option to skip
    # pages. By default, if skip_until_the_end_of = "experiment", if he decides to skip pages, he will skip all the
    # pages until the end of the experiment (provided those pages inherit from SkippablePage or LeavableWaitPage).
    # If skip_until_the_end_of = "app", he will only skip the pages of the current app.
    # If skip_until_the_end_of = "round", only pages of the current round will be skipped
    allow_leaving_after = 3600
    # "experiment" or "app or "round"
    skip_until_the_end_of = "experiment"
    group_by_arrival_time = True

    use_task = False
    task = "sliders_task"  # Available options: sliders_task, arithmetic_tasks, survey

    pay_by_task = False
    pay_by_time = False

    max_bonus_for_page = None



    def dispatch(self, *args, **kwargs):
        curparticipant = Participant.objects.get(code__exact=kwargs['participant_code'])

        if self.request.method == 'POST':
            app_name = curparticipant._current_app_name
            index_in_pages = curparticipant._index_in_pages
            now = time.time()
            wptimerecord = models.WPTimeRecord.objects.get(app=app_name, page_index=index_in_pages,
                                                           augmented_participant_id=curparticipant.id)
            time_left = wptimerecord.startwp_time + self.allow_leaving_after - now

            if time_left > 0:
                url_should_be_on = curparticipant._url_i_should_be_on()
                return HttpResponseRedirect(url_should_be_on)

            if self.skip_until_the_end_of in ["app", "round"]:
                app_name = curparticipant._current_app_name
                if self.skip_until_the_end_of == "round":
                    round_number = curparticipant._round_number
                    curparticipant.vars['skip_the_end_of_app_{}_round_{}'.format(app_name, round_number)] = True
                else:
                    # "app"
                    curparticipant.vars['skip_the_end_of_app_{}'.format(app_name)] = True
            else:
                assert self.skip_until_the_end_of == "experiment", \
                    "the attribute skip_until_the_end_of should be set to experiment, app or round, not {}".format(
                        self.skip_until_the_end_of)
                curparticipant.vars['go_to_the_end'] = True

            curparticipant.save()
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_name = self.player._meta.app_label
        index_in_pages = self._index_in_pages
        now = time.time()

        wptimerecord, timerecord_created = self.participant.augmentedparticipant.wptimerecord_set.get_or_create(app=app_name,
                                                                                                     page_index=index_in_pages)
        if not wptimerecord.startwp_timer_set:
            wptimerecord.startwp_timer_set = True
            wptimerecord.startwp_time = time.time()
            wptimerecord.save()
        time_left = wptimerecord.startwp_time + self.allow_leaving_after - now
        time_passed = now - wptimerecord.startwp_time

        wpslidersrecord, slidersrecord_created = self.participant.augmentedparticipant.waitingroomsliderstaskrecord_set.get_or_create(app=app_name,
                                                                                                     page_index=index_in_pages)
        if self.task == "sliders_task":
            if not wpslidersrecord.sliders_task_set:
                wpslidersrecord.sliders_task_set = True
                sliders_offsets, sliders_curr_values, sliders_for_task = \
                    create_sliders_task(num_sliders, slider_columns, sliders_min, middle_value, sliders_max)
                wpslidersrecord.sliders_offsets = json.dumps(sliders_offsets)
                wpslidersrecord.sliders_curr_values = json.dumps(sliders_curr_values)
                wpslidersrecord.sliders_for_task = json.dumps(sliders_for_task)
                wpslidersrecord.num_centered_sliders = len([v for v in sliders_curr_values if v == middle_value])
                wpslidersrecord.bonus_per_slider = self.session.config['bonus_per_slider'] if self.session.config.get('bonus_per_slider') else 0.02
                wpslidersrecord.save()

            sliders_offsets = json.loads(wpslidersrecord.sliders_offsets)
            sliders_curr_values = json.loads(wpslidersrecord.sliders_curr_values)
            sliders_for_task = create_sliders_task(num_sliders, slider_columns, sliders_min, middle_value, sliders_max, sliders_offsets, sliders_curr_values)[2]
            num_centered_sliders = wpslidersrecord.num_centered_sliders
            bonus_per_slider = wpslidersrecord.bonus_per_slider
            bonus_for_sliders_task = num_centered_sliders * bonus_per_slider
            task_for_template = {
                'sliders_for_task': sliders_for_task,
                'middle_value': middle_value,
                'sliders_min': sliders_min,
                'sliders_max': sliders_max,
                'num_centered_sliders': num_centered_sliders,
                'bonus_per_slider': bonus_per_slider,
                'bonus_for_sliders_task': "{0:.2f}".format(bonus_for_sliders_task)
            }


        context.update({
            'index_in_pages': index_in_pages,
            'time_left': round(time_left),
            'time_passed': round(time_passed),
            'app_name': app_name,
            'task_for_template': task_for_template

        })
        return context

    def __init__(self):
        super(LeavableWaitPage, self).__init__()

        # IS A WAIT PAGE
        def decorate_after_all_players_arrive(func):
            def decorated_after_all_players_arrive(*args, **kwargs):
                self.extra_task_to_decorate_start_of_after_all_players_arrive()
                func(*args, **kwargs)
                self.extra_task_to_decorate_end_of_after_all_players_arrive()

            return decorated_after_all_players_arrive

        setattr(self, "after_all_players_arrive",
                decorate_after_all_players_arrive(getattr(self, "after_all_players_arrive")))

        # We need to edit is_displayed() method dynamically, when creating an instance, since custom use is that it is
        # overriden in the last child
        def decorate_is_displayed(func):
            def decorated_is_display(*args, **kwargs):
                game_condition = func(*args, **kwargs)
                # we need to first run them both separately to make sure that both conditions are executed
                self.extra_task_to_execute_with_is_display()
                return game_condition

            return decorated_is_display

        setattr(self, "is_displayed", decorate_is_displayed(getattr(self, "is_displayed")))

        def decorate_get_players_for_group(func):
            def decorated_get_players_for_group(*args, **kwargs):
                grouped = self.extra_task_to_decorate_start_of_get_players_for_group(*args, **kwargs)
                if grouped:
                    # form groups of only one when a players decides to finish the experiment--> otherwise,
                    # there might be problems later during ordinary wait pages
                    return grouped[0:1]
                grouped = func(*args, **kwargs)
                if grouped:
                    return grouped
                grouped = self.extra_task_to_decorate_end_of_get_players_for_group(*args, **kwargs)
                if grouped:
                    return grouped

            return decorated_get_players_for_group

        setattr(self, "get_players_for_group",
                decorate_get_players_for_group(getattr(self, "get_players_for_group")))

    def extra_task_to_decorate_start_of_get_players_for_group(self, waiting_players):
        app_name = self.subsession._meta.app_label
        round_number = self.subsession.round_number
        endofgamers = [p for p in waiting_players if (
                p.participant.vars.get('go_to_the_end') or p.participant.vars.get(
            'skip_the_end_of_app_{}'.format(app_name)) or p.participant.vars.get(
            'skip_the_end_of_app_{}_round_{}'.format(app_name, round_number))
        )]
        if endofgamers:
            return endofgamers

    def extra_task_to_decorate_end_of_get_players_for_group(self, waiting_players):
        pass

    def extra_task_to_decorate_start_of_after_all_players_arrive(self):
        pass

    def extra_task_to_decorate_end_of_after_all_players_arrive(self):
        if self.wait_for_all_groups:
            players = self.subsession.get_players()
        else:
            players = self.group.get_players()
        # It is theoretically possible to have a participant with "go_to_the_end" and also inside a "normal" group with
        # more than one player... This can happen because "go_to_the_end" is set outside of the group-by-arrival-time
        # lock (and the lock varies depending on the version of oTree so we can not easily fix this), but should be
        # very rare, just when a participant requests exits right at the moment when he is grouped and if we have no
        # luck...
        # To fix this, we use a dirty hack here... we detect this anomaly with this test
        if len(players) > 1:
            app_name = players[0]._meta.app_label
            round_number = players[0].round_number
            for p in players:
                exiter = p.participant.vars.get('go_to_the_end', False) or p.participant.vars.get(
                    'skip_the_end_of_app_{}'.format(app_name), False) or p.participant.vars.get(
                    'skip_the_end_of_app_{}_round_{}'.format(app_name, round_number), False)
                if exiter:
                    # --> fix the error, remove the exit marker
                    p.participant.vars.pop('go_to_the_end', None)
                    p.participant.vars.pop('skip_the_end_of_app_{}'.format(app_name), None)
                    p.participant.vars.pop('skip_the_end_of_app_{}_round_{}'.format(app_name, round_number), None)

    def extra_task_to_execute_with_is_display(self):
        self.participant.vars.setdefault('starting_time_stamp_{}'.format(self._index_in_pages), time.time())
