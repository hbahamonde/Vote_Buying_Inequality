from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class PreIntro(Page):
    timeout_seconds = 240

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanza_vs_1 = True


class PreIntro2(Page):
    timeout_seconds = 240

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanza_vs_2 = True


class Intro(Page):
    timeout_seconds = 240
    form_fields = ['p_oferta_choice_A', "p_oferta_choice_B", "p_oferta_amount_A", "p_oferta_amount_B"]
    form_model = 'player'

    def is_displayed(self):
        return self.player.votanteOpartido == "votantes"

    def error_message(self, value):
        if value['p_oferta_amount_A'] > self.group.presupuesto or value['p_oferta_amount_B'] > self.group.presupuesto:
            return 'La oferta no puede exceder el presupuesto'

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
        if self.player.id_in_group == 1:
            if self.player.p_oferta_amount_A != 0:
                self.player.p_oferta_choice_A = True
            else:
                self.player.p_oferta_choice_A = False

            if self.player.p_oferta_amount_B != 0:
                self.player.p_oferta_choice_B = True
            else:
                self.player.p_oferta_choice_B = False

        if self.timeout_happened:
            self.player.avanza_vs_3 = True


class Intro2(Page):
    timeout_seconds = 240
    def is_displayed(self):
        return self.player.votanteOpartido == "Partido A" or self.player.votanteOpartido == "Partido B"

    def vars_for_template(self):
        return dict(
            N=self.group.n_votantes,
            partido=self.player.votanteOpartido,
            partido_votante=self.group.get_player_by_id(1).tipoAoB,
            pje_A=self.group.pje_win_cA,
            pje_B=self.group.pje_win_cB,
            n_pa=self.group.n_votantes_A,
            n_pb=self.group.n_votantes_B,
            presupuesto=self.group.presupuesto
        )

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanza_vs_4 = True


class Espera(Page):
    timeout_seconds = 240

    def vars_for_template(self):
        return dict(
            mi_partido=self.player.votanteOpartido,
        )

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanza_vs_5 = True


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Offers(Page):
    timeout_seconds = 240
    form_fields = ['partido_envia_puntos']
    form_model = 'player'

    def is_displayed(self):
        return self.player.votanteOpartido == "Partido A" or self.player.votanteOpartido == "Partido B"

    def vars_for_template(self):
        return dict(
            N=self.group.n_votantes,
            tipo_partido=self.group.get_player_by_id(1).tipoAoB,
            oferta_PA=self.group.get_player_by_id(1).p_oferta_amount_A,
            oferta_PB=self.group.get_player_by_id(1).p_oferta_amount_B,
            mi_partido=self.player.votanteOpartido,
            pje_A=self.group.pje_win_cA,
            pje_B=self.group.pje_win_cB,
            n_pa=self.group.n_votantes_A,
            n_pb=self.group.n_votantes_B,
            presupuesto=self.group.presupuesto,
            partido=self.player.votanteOpartido,
        )

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanza_vs_6 = True


class Offers2(Page):
    timeout_seconds = 240
    form_fields = ['votante_acepta_oferta']
    form_model = 'player'

    def is_displayed(self):
        return self.player.votanteOpartido == "votantes"

    def vars_for_template(self):
        if self.group.n_votantes_A >= self.group.n_votantes_B:
            candidato="A"
        else:
            candidato = "B"

        return dict(
            tipo_partido=self.player.tipoAoB,
            oferta_PA=self.group.get_player_by_id(1).p_oferta_amount_A,
            oferta_PB=self.group.get_player_by_id(1).p_oferta_amount_B,
            pje_A=self.group.pje_win_cA,
            pje_B=self.group.pje_win_cB,
            partido_gana_antes_votacion=candidato,
            presupuesto=self.group.presupuesto,
            A_envia_puntos=self.group.get_player_by_id(2).partido_envia_puntos,
            B_envia_puntos=self.group.get_player_by_id(3).partido_envia_puntos,
            oferta_acepta=self.group.get_player_by_id(1).votante_acepta_oferta,
        )

    def before_next_page(self):
        if self.timeout_happened:
            self.player.avanza_vs_7 = True


class NormalWaitPage(WaitPage):
    pass


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_vot_payoff()


class Results(Page):
    timeout_seconds = 240

    def vars_for_template(self):
        return dict(
            partido_elegido=self.group.partido_elegido,
            puntaje_total=self.player.puntos,
            oferta_acepta=self.group.get_player_by_id(1).votante_acepta_oferta,
            pa_envia_puntos=self.group.get_player_by_id(2).partido_envia_puntos,
            pb_envia_puntos=self.group.get_player_by_id(3).partido_envia_puntos,
            win_lose=self.player.win_lose,
            win_losev=self.player.win_losev,
            tipo_partido=self.group.get_player_by_id(1).tipoAoB,
            mi_partido=self.player.votanteOpartido,
            votante_gano=self.group.get_player_by_id(1).puntos,
            PA_gano=self.group.get_player_by_id(2).puntos,
            PB_gano=self.group.get_player_by_id(3).puntos,
            oferta_a=self.group.get_player_by_id(1).p_oferta_amount_A,
            oferta_b=self.group.get_player_by_id(1).p_oferta_amount_B,
        )

    def before_next_page(self):
        self.player.payoff = self.player.puntos * Constants.exchange_rate

        if self.round_number == 3:
            self.participant.vars['votos_s'] = sum([p.payoff for p in self.player.in_all_rounds()])
            print(self.participant.vars['votos_s'])

        if self.timeout_happened:
            self.player.avanza_vs_8 = True


page_sequence = [
    Intro,
    Intro2,
    NormalWaitPage,
    Espera,
    Offers,
    NormalWaitPage,
    Offers2,
    ResultsWaitPage,
    Results]
