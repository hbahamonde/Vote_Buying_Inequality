# coding=utf-8
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Mauricio López T'

doc = """
Cuestionario
"""


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.StringField(label='Nombre:')
    q2 = models.StringField(label='Email:')
    q3 = models.StringField(choices=['Hombre', 'Mujer', 'Otro'],
                            label='Género',
                            widget=widgets.RadioSelect)
    q4 = models.IntegerField(widget=widgets.RadioSelect,
                             choices=[[1, 'Les alcanza bien y pueden ahorrar'],
                                      [2, 'Les alcanza justo y sin grandes dificultades'],
                                      [3, 'No les alcanza y tienen dificultades'],
                                      [4, 'No les alcanza y tienen grandes dificultades']],
                             label='El salario o sueldo que usted recibe y el total del ingreso de su hogar')

    q5 = models.IntegerField(widget=widgets.RadioSelect,
                              choices=[[1, 'Menos de $288.800'], [2, 'Entre $288.801 - $312.001'],
                                       [3, 'Entre $312.002 - $361.002'], [4, 'Entre $361.003 - $410.003'],
                                       [5, 'Entre $410.004 - $459.004'], [6, 'Entre $459.005 - $558.005'],
                                       [7, 'Entre $558.006 - $657.006'], [8, 'Entre $657.007 - $756.007'],
                                       [9, 'Entre $756.008 - $1.005.008'], [10, 'Más de $1.005.008']],
                             label='A continuación, hay varios rangos de ingresos. Indique en cuál de los siguientes '
                                    'rangos está el ingreso que usted personalmente gana al mes por su trabajo o pensión,'
                                    'sin contar el resto de los ingresos del hogar' )

    q6 = models.BooleanField(widget=widgets.RadioSelectHorizontal, choices=[[1, 'Sí'],[0, 'No']],
                             label='En este momento ¿simpatiza con algún partido político?' )

    q7 = models.IntegerField(widget=widgets.RadioSelect,
                              choices=[[1, 'Partido Socialista de Chile'],
                                       [2, 'Unión Demócrata Independiente'],
                                       [3, 'Renovación Nacional'],
                                       [4, 'Partido Demócrata Cristiano'],
                                       [5, 'Partido Comunistica de Chile'],
                                       [6, 'Revolución Democrática'],
                                       [7, 'Evolución Política'],
                                       [8, 'Otro'],
                                       [9, 'No me siento representado']],
                             label='¿Con cuál partido político simpatiza usted?' )

    q8 = models.IntegerField(widget=widgets.RadioSelectHorizontal, choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                             label='Cambiando de tema, tenemos una escala de 1 a 10 que va de izquierda a derecha, '
                                   'en la que 1 significa izquierda y el 10 derecha. Hoy en día cuando se habla de '
                                   'tendencias políticas, mucha gente habla de aquellos que simpatizan más con la '
                                   'izquierda o con la derecha. Según el sentido que tengan para usted los términos '
                                   '"izquierda" y "derecha" cuando piensa sobre su punto de vista político, ¿dónde se '
                                   'encontraría usted en esta escala?. '
                                   'Marca el número que representa tu ideología política.' )

    q9 = models.BooleanField(choices=[[1, 'Sí'],[0, 'No']],
                            label='Ahora pensando en las elecciones políticas, a cualquier cargo sujeto a votación popular, '
                                  '¿Votaste en la última elección?',
                            widget=widgets.RadioSelectHorizontal)

    q10 = models.BooleanField(choices=[[1, 'Sí'],[0, 'No']],
                            label='¿Piensas votar en la próxima elección?',
                            widget=widgets.RadioSelectHorizontal)
