# coding=utf-8
from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range
)
import random
import math

author = 'Mauricio López T'

doc = """
Vote selling
"""


class Constants(BaseConstants):
    name_in_url = 'vote_s'
    players_per_group = 3
    num_rounds = 3
    D = 2000 # utilidad del votante
    E = 2400 # Puntos por ganar eleccion
    exchange_rate = 5/12


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.get_votantes()
            self.get_presupuesto()
        else:
            matrix = self.get_group_matrix()
            for row in matrix:
                random.shuffle(row)
                self.set_group_matrix(matrix)
            self.get_votantes()
            self.get_presupuesto()

    def get_presupuesto(self):
        groups = self.get_groups()
        for g in groups:
            g.presupuesto = int(random.uniform(900,1800))
            g.n_votantes = random.choice([3, 5])

            #Votantes ficticios por grupo
            if g.n_votantes == 3:
                vot_extrasA = math.floor(2 * random.random()) + 1
            elif g.n_votantes == 5:
                vot_extrasA = math.floor(4 * random.random()) + 1
            vot_extrasB = g.n_votantes - vot_extrasA

            g.n_votantes_A = g.n_votantes_A + vot_extrasA
            g.n_votantes_B = g.n_votantes_B + vot_extrasB

            if g.n_votantes_A > g.n_votantes_B:
                g.partido_elegido = "Partido A"
            else:
                g.partido_elegido = "Partido B"

    def get_votantes(self):
        player = self.get_players()
        groups = self.get_groups()
        for g in groups:
            g.ubicacion_pA = int(random.uniform(1, 50)) #confirmar
            g.ubicacion_pB = int(random.uniform(51, 100)) #confirmar
            g.tipo_votante = int(random.uniform(1, 100))  # confirmar
            g.pje_win_cA = Constants.D - 20 * (abs(g.tipo_votante - g.ubicacion_pA))
            g.pje_win_cB = Constants.D - 20 * (abs(g.tipo_votante - g.ubicacion_pB))

        for p in player:
            if p.id_in_group == 1:
                p.votanteOpartido = "votantes"
                if g.tipo_votante > 50:
                    p.tipoAoB = "B"
                else:
                    p.tipoAoB = "A"
            elif p.id_in_group == 2:
                p.votanteOpartido = "Partido A"
            elif p.id_in_group == 3:
                p.votanteOpartido = "Partido B"


class Group(BaseGroup):
    presupuesto = models.IntegerField(initial=0)
    n_votantes = models.IntegerField(initial=0)
    n_votantes_A = models.IntegerField(initial=0)
    n_votantes_B = models.IntegerField(initial=0)
    partido_elegido = models.StringField()
    tipo_votante = models.IntegerField(initial=0)
    ubicacion_pA = models.IntegerField(initial=0)
    ubicacion_pB = models.IntegerField(initial=0)
    pje_win_cA = models.IntegerField(initial=0)
    pje_win_cB = models.IntegerField(initial=0)

    def set_vot_payoff(self):
        player = self.get_players()
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)

        for p in player:
            if p.id_in_group == 1:
                if p.tipoAoB == "A" and p.votante_acepta_oferta == 1:
                    if self.n_votantes_A > self.n_votantes_B:
                        self.partido_elegido = "Partido A"
                        p.win_losev = "ganó"
                        if p2.partido_envia_puntos == 1:
                            p.puntos = self.pje_win_cA + p.p_oferta_amount_A
                        else:
                            p.puntos = self.pje_win_cA
                    else:
                        self.partido_elegido = "Partido B"
                        p.win_losev = "perdió"
                        if p2.partido_envia_puntos == 1:
                            p.puntos = self.pje_win_cB + p.p_oferta_amount_A
                        else:
                            p.puntos = self.pje_win_cB
                elif p.tipoAoB == "A" and p.votante_acepta_oferta == 2:
                    if p.p_oferta_amount_B > 0:
                        votantes_a = self.n_votantes_A - 1
                        votantes_b = self.n_votantes_B + 1
                        if votantes_a > votantes_b:
                            self.partido_elegido = "Partido A"
                            p.win_losev = "perdió"
                            if p3.partido_envia_puntos == 1:
                                p.puntos = self.pje_win_cA + self.p_oferta_amount_B
                            else:
                                p.puntos = self.pje_win_cA
                        else:
                            self.partido_elegido = "Partido B"
                            p.win_losev = "ganó"
                            if p3.partido_envia_puntos == 1:
                                p.puntos = self.pje_win_cB + p1.p_oferta_amount_B
                            else:
                                p.puntos = self.pje_win_cB
                    else:
                        if self.n_votantes_A > self.n_votantes_B:
                            self.partido_elegido = "Partido A"
                            p.win_losev = "ganó"
                            p.puntos = self.pje_win_cA
                        else:
                            self.partido_elegido = "Partido B"
                            p.win_losev = "perdió"
                            p.puntos = self.pje_win_cB
                elif p.tipoAoB == "B" and p.votante_acepta_oferta == 1:
                    if p.p_oferta_amount_A > 0:
                        votantes_a = self.n_votantes_A + 1
                        votantes_b = self.n_votantes_B - 1
                        if votantes_a > votantes_b:
                            self.partido_elegido = "Partido A"
                            p.win_losev = "ganó"
                            if p2.partido_envia_puntos == 1:
                                p.puntos = self.pje_win_cA + p.p_oferta_amount_A
                            else:
                                p.puntos = self.pje_win_cA
                        else:
                            self.partido_elegido = "Partido B"
                            p.win_losev = "perdió"
                            if p2.partido_envia_puntos == 1:
                                p.puntos = self.pje_win_cB + p.p_oferta_amount_A
                            else:
                                p.puntos = self.pje_win_cB
                    else:
                        if self.n_votantes_A > self.n_votantes_B:
                            self.partido_elegido = "Partido A"
                            p.win_losev = "perdió"
                            p.puntos = self.pje_win_cA
                        else:
                            self.partido_elegido = "Partido B"
                            p.win_losev = "ganó"
                            p.puntos = self.pje_win_cB
                elif p.tipoAoB == "B" and p.votante_acepta_oferta == 2:
                    if self.n_votantes_A > self.n_votantes_B:
                        self.partido_elegido = "Partido A"
                        p.win_losev = "perdió"
                        if p3.partido_envia_puntos == 1:
                            p.puntos = self.pje_win_cA + p.p_oferta_amount_B
                        else:
                            p.puntos = self.pje_win_cA
                    else:
                        self.partido_elegido = "Partido B"
                        p.win_losev = "ganó"
                        if p3.partido_envia_puntos == 1:
                            p.puntos = self.pje_win_cB + p.p_oferta_amount_B
                        else:
                            p.puntos = self.pje_win_cB
                elif p.votante_acepta_oferta == 3 or p.votante_acepta_oferta is None:
                    if self.n_votantes_A > self.n_votantes_B:
                        self.partido_elegido = "Partido A"
                        p.puntos = self.pje_win_cA
                        if p.tipoAoB == "A":
                            p.win_losev = "ganó"
                        else:
                            p.win_losev = "perdió"
                    else:
                        self.partido_elegido = "Partido B"
                        p.puntos = self.pje_win_cB
                        if p.tipoAoB == "A":
                            p.win_losev = "perdió"
                        else:
                            p.win_losev = "ganó"
            else:
                if p.partido_envia_puntos == 1:
                    if self.partido_elegido == "Partido A" and p1.votante_acepta_oferta == 1:
                        if p.votanteOpartido == "Partido A":
                            p.win_lose = "ganó"
                            p.puntos = Constants.E + (self.presupuesto - p1.p_oferta_amount_A)
                        else:
                            p.puntos = self.presupuesto
                            p.win_lose = "perdió"
                    elif self.partido_elegido == "Partido A" and p1.votante_acepta_oferta == 2:
                        if p.votanteOpartido == "Partido A":
                            p.win_lose = "ganó"
                            p.puntos = Constants.E + self.presupuesto
                        else:
                            p.puntos = self.presupuesto - p1.p_oferta_amount_B
                            p.win_lose = "perdió"
                    elif self.partido_elegido == "Partido B" and p1.votante_acepta_oferta == 1:
                        if p.votanteOpartido == "Partido A":
                            p.puntos = self.presupuesto - p1.p_oferta_amount_A
                            p.win_lose = "perdió"
                        else:
                            p.win_lose = "ganó"
                            p.puntos = Constants.E + self.presupuesto
                    elif self.partido_elegido == "Partido B" and p1.votante_acepta_oferta == 2:
                        if p.votanteOpartido == "Partido B":
                            p.win_lose = "ganó"
                            p.puntos = Constants.E + self.presupuesto - p1.p_oferta_amount_B
                        else:
                            p.puntos = self.presupuesto
                            p.win_lose = "perdió"
                    elif self.partido_elegido == "Partido B" and p1.votante_acepta_oferta == 2:
                        if p.votanteOpartido == "Partido B":
                            p.win_lose = "ganó"
                            p.puntos = Constants.E + self.presupuesto - p1.p_oferta_amount_B
                        else:
                            p.puntos = self.presupuesto
                            p.win_lose = "perdió"
                    elif p1.votante_acepta_oferta == 3 or p1.votante_acepta_oferta is None:
                        if self.partido_elegido == "Partido A":
                            if p.votanteOpartido == "Partido A":
                                p.puntos = Constants.E + self.presupuesto
                                p.win_lose = "ganó"
                            else:
                                p.puntos = self.presupuesto
                                p.win_lose = "perdió"
                        elif self.partido_elegido == "Partido B":
                            if p.votanteOpartido == "Partido A":
                                p.puntos = self.presupuesto
                                p.win_lose = "perdió"
                            else:
                                p.puntos = Constants.E + self.presupuesto
                                p.win_lose = "ganó"
                else:
                    if self.partido_elegido == "Partido A" and p1.votante_acepta_oferta == 1:
                        if p.votanteOpartido == "Partido A":
                            p.win_lose = "ganó"
                            p.puntos = Constants.E + self.presupuesto
                        else:
                            p.puntos = self.presupuesto
                            p.win_lose = "perdió"
                    elif self.partido_elegido == "Partido A" and p1.votante_acepta_oferta == 2:
                        if p.votanteOpartido == "Partido A":
                            p.win_lose = "ganó"
                            p.puntos = Constants.E + self.presupuesto
                        else:
                            p.puntos = self.presupuesto
                            p.win_lose = "perdió"
                    elif self.partido_elegido == "Partido B" and p1.votante_acepta_oferta == 1:
                        if p.votanteOpartido == "Partido A":
                            p.puntos = self.presupuesto
                            p.win_lose = "perdió"
                        else:
                            p.win_lose = "ganó"
                            p.puntos = Constants.E + self.presupuesto
                    elif self.partido_elegido == "Partido B" and p1.votante_acepta_oferta == 2:
                        if p.votanteOpartido == "Partido B":
                            p.win_lose = "ganó"
                            p.puntos = Constants.E + self.presupuesto
                        else:
                            p.puntos = self.presupuesto
                            p.win_lose = "perdió"
                    elif self.partido_elegido == "Partido B" and p1.votante_acepta_oferta == 2:
                        if p.votanteOpartido == "Partido B":
                            p.win_lose = "ganó"
                            p.puntos = Constants.E + self.presupuesto
                        else:
                            p.puntos = self.presupuesto
                            p.win_lose = "perdió"
                    elif p1.votante_acepta_oferta == 3 or p1.votante_acepta_oferta is None:
                        if self.partido_elegido == "Partido A":
                            if p.votanteOpartido == "Partido A":
                                p.puntos = Constants.E + self.presupuesto
                                p.win_lose = "ganó"
                            else:
                                p.puntos = self.presupuesto
                                p.win_lose = "perdió"
                        elif self.partido_elegido == "Partido B":
                            if p.votanteOpartido == "Partido A":
                                p.puntos = self.presupuesto
                                p.win_lose = "perdió"
                            else:
                                p.puntos = Constants.E + self.presupuesto
                                p.win_lose = "ganó"


class Player(BasePlayer):
    votanteOpartido = models.StringField()
    tipoAoB = models.StringField()

    p_oferta_choice_A = models.BooleanField(choices=[
        [True, "Si, quiero negociar con el partido A: "],
        [False, "No, no quiero negociar con el partido A."]], blank=True, null=True)

    p_oferta_choice_B = models.BooleanField(choices=[
        [True, "Si, quiero negociar con el partido B: "],
        [False, "No, no quiero negociar con el partido B."]], blank=True, null=True)

    p_oferta_amount_A = models.IntegerField(initial=0, min=0, blank=True, null=True)
    p_oferta_amount_B = models.IntegerField(initial=0, min=0, blank=True, null=True)

    partido_envia_puntos = models.BooleanField(
        choices=[
            [True, "Sí"],
            [False, "No."]
        ],
        widget=widgets.RadioSelect, blank=True)

    votante_acepta_oferta = models.IntegerField(
        choices=[
            [1, "Los puntos del partido A."],
            [2, "Los puntos del partido B."],
            [3, "Ninguna oferta; no quiero aceptar puntos a cambio de mi voto."]
        ],
        widget=widgets.RadioSelect, blank=True)

    win_lose = models.StringField()
    win_losev = models.StringField()
    puntos = models.IntegerField(initial=0)

    def grabar_eleccionA(self):
        self.p_oferta_choice_A = True

    def grabar_eleccionB(self):
        self.p_oferta_choice_B = True

    def role(self):
        if self.id_in_group == 1:
            return 'votantes'
        else:
            return 'Partido'

    avanza_vs_1 = models.BooleanField()
    avanza_vs_2 = models.BooleanField()
    avanza_vs_3 = models.BooleanField()
    avanza_vs_4 = models.BooleanField()
    avanza_vs_5 = models.BooleanField()
    avanza_vs_6 = models.BooleanField()
    avanza_vs_7 = models.BooleanField()
    avanza_vs_8 = models.BooleanField()
