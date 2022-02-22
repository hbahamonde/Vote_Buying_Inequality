from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    nombre_session="nombre de la sesion", real_world_currency_per_point=0.42, participation_fee=2000, doc=""
)

SESSION_CONFIGS = [
    {
        'name': 'voting',
        'display_name': "vote-buying",
        'num_demo_participants': 3,
        'app_sequence': ['consent','testing_round_1', 'vote_b','survey', 'payment'],
    },
    {
        'name': 'voting2',
        'display_name': "vote-selling",
        'num_demo_participants': 3,
        'app_sequence': ['consent', 'testing_round_2', 'vote_s','survey', 'payment_s'],
    },
    {
        'name': 'survey',
        'display_name': "survey",
        'num_demo_participants': 1,
        'app_sequence': ['survey'],
    },
    {
        'name': 'testing_round_1',
        'display_name': "Ensayo vote buying",
        'num_demo_participants': 1,
        'app_sequence': ['testing_round_1'],
    },
    {
        'name': 'testing_round_2',
        'display_name': "Ensayo vote selling",
        'num_demo_participants': 1,
        'app_sequence': ['testing_round_2'],
    },
    {
        'name': 'votos_completo',
        'display_name': "Juego Completo",
        'num_demo_participants': 3,
        'app_sequence': ['consent', 'testing_round_1', 'vote_b','testing_round_2', 'vote_s', 'survey', 'payment_s'],
    }
    # dict(
    #    name='public_goods',
    #    display_name="Public Goods",
    #    num_demo_participants=3,
    #    app_sequence=['public_goods', 'payment_info']
    # ),
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'es'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'CLP'
USE_POINTS = False
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 0

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """Recreating Market Conditions for Vote-Selling and Vote-Buying in the Lab: The Chilean Case """

SECRET_KEY = 'zp(r#irj^_r512h6a3x+5nnanr&v@#$x&2w5_32ck!7d)m($c-'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree', 'django.contrib.humanize']
EXTENSION_APPS = ['leavable_wait_page']
#EXTENSION_APPS = ['leavable_wait_page']
