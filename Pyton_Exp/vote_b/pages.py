from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from leavable_wait_page.pages import SkippablePage, LeavableWaitPage


class Intro(Page):
    timeout_seconds = 240
    def is_displayed(self):
        return self.player.votanteOpartido == "votantes"

    def vars_for_template(self):
        if self.player.tipoAoB == 'A':
            return dict(
                N=self.group.n_votantes,
                N2=self.group.n_votantes - 1,
                partido=self.player.tipoAoB,
                pje_A=self.group.pje_win_cA,
                pje_B=self.group.pje_win_cB,
                n_pa=self.group.n_votantes_A - 1,
                n_pb=self.group.n_votantes_B,
                max_pg=self.group.presupuesto
            )
        else:
            return dict(
                N=self.group.n_votantes,
                N2=self.group.n_votantes - 1,
                partido=self.player.tipoAoB,
                pje_A=self.group.pje_win_cA,
                pje_B=self.group.pje_win_cB,
                n_pa=self.group.n_votantes_A,
                n_pb=self.group.n_votantes_B - 1,
                max_pg=self.group.presupuesto
            )

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanza_vb_1 = True


class Intro2(Page):
    timeout_seconds = 240
    form_fields = ['p_oferta_choice', "p_oferta_amount"]
    form_model = 'player'

    def is_displayed(self):
        return self.player.votanteOpartido == "Partido A" or self.player.votanteOpartido == "Partido B"

    def error_message(self, value):
        print('Ingresaste', value)
        if value['p_oferta_amount'] > self.group.presupuesto:
            return 'La oferta no puede exceder el presupuesto'

    def vars_for_template(self):
        return dict(
            N=self.group.n_votantes,
            partido=self.player.votanteOpartido,
            partido_votante=self.group.get_player_by_id(1).tipoAoB,
            pje_A='{:,}'.format(self.group.pje_win_cA).replace(',','.'),
            pje_B='{:,}'.format(self.group.pje_win_cB).replace(',','.'),
            n_pa=self.group.n_votantes_A,
            n_pb=self.group.n_votantes_B,
            presupuesto=self.group.presupuesto
        )

    def before_next_page(self):
        if self.player.id_in_group != 1:
            if self.player.p_oferta_amount == 0:
                self.player.p_oferta_choice = 0
            else:
                self.player.p_oferta_choice = 1

        if self.timeout_happened:
            self.player.avanza_vb_2 = True


class Espera(Page):
    timeout_seconds = 240

    def vars_for_template(self):
        return dict(
            mi_partido=self.player.votanteOpartido,
        )

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanza_vb_3 = True


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Offers(Page):
    timeout_seconds = 240
    form_fields = ['p_oferta_acepta']
    form_model = 'player'

    def is_displayed(self):
        return self.player.votanteOpartido == "votantes"

    def vars_for_template(self):
        return dict(
            tipo_partido=self.player.tipoAoB,
            pje_A=self.group.pje_win_cA,
            pje_B=self.group.pje_win_cB,
            oferta_PA=self.group.get_player_by_id(2).p_oferta_amount,
            oferta_PB=self.group.get_player_by_id(3).p_oferta_amount,
            presupuesto=self.group.presupuesto,
            partido=self.player.votanteOpartido,
        )

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanza_vb_4 = True


class NormalWaitPage(WaitPage):
    pass


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_vot_payoff()


class Results(Page):
    timeout_seconds = 240
    def vars_for_template(self):
        if self.group.partido_elegido == 'A':
            return dict(
                partido_elegido=self.group.partido_elegido,
                puntaje_total=self.player.puntos,
                puntaje_total_pa=self.group.get_player_by_id(2).puntos,
                puntaje_total_pb=self.group.get_player_by_id(3).puntos,
                oferta_acepta=self.group.get_player_by_id(1).p_oferta_acepta,
                oferta_a=self.group.get_player_by_id(2).p_oferta_amount,
                oferta_b=self.group.get_player_by_id(3).p_oferta_amount,
                win_lose=self.player.win_lose,
                tipo_partido=self.group.get_player_by_id(1).tipoAoB,
                nuevo_tipopartido=self.group.get_player_by_id(1).nuevotipoAoB,
                mi_partido=self.player.votanteOpartido,
                votante_gano=self.group.get_player_by_id(1).puntos
            )
        else:
            return dict(
                partido_elegido=self.group.partido_elegido,
                puntaje_total=self.player.puntos,
                puntaje_total_pa=self.group.get_player_by_id(2).puntos,
                puntaje_total_pb=self.group.get_player_by_id(3).puntos,
                oferta_acepta=self.group.get_player_by_id(1).p_oferta_acepta,
                oferta_a=self.group.get_player_by_id(2).p_oferta_amount,
                oferta_b=self.group.get_player_by_id(3).p_oferta_amount,
                win_lose=self.player.win_lose,
                tipo_partido=self.group.get_player_by_id(1).tipoAoB,
                nuevo_tipopartido=self.group.get_player_by_id(1).nuevotipoAoB,
                mi_partido=self.player.votanteOpartido,
                votante_gano=self.group.get_player_by_id(1).puntos
            )

    def before_next_page(self):
        self.player.payoff = self.player.puntos * Constants.exchange_rate

        if self.round_number == 3:
            self.participant.vars['votos_b'] = sum([p.payoff for p in self.player.in_all_rounds()])
            print(self.participant.vars['votos_b'])

        if self.timeout_happened:
            self.player.avanza_vb_5 = True


page_sequence = [Intro, Intro2, NormalWaitPage, Espera, Offers, ResultsWaitPage,  Results]
