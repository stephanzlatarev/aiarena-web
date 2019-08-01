from django.core.files import File
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from aiarena import settings
from aiarena.core.models import User, Map, Bot, Match, Result
from aiarena.core.tests import BaseTestCase
from aiarena.core.utils import EnvironmentType


def create_match(as_user):
    return Match.start_next_match(as_user)


def create_result_with_bot_data_and_logs(match, type, as_user):
    with open(BaseTestCase.test_replay_path, 'rb') as result_replay, \
            open(BaseTestCase.test_bot1_data_path, 'rb') as bot1_data, \
            open(BaseTestCase.test_bot2_data_path, 'rb') as bot2_data, \
            open(BaseTestCase.test_bot1_match_log_path, 'rb') as bot1_log, \
            open(BaseTestCase.test_bot2_match_log_path, 'rb') as bot2_log:
        result = Result.objects.create(match=match, type=type, replay_file=File(result_replay), game_steps=1,
                                       submitted_by=as_user)
        result.finalize_submission(File(bot1_data), File(bot2_data), File(bot1_log), File(bot2_log), 0.111111, 0.222222)


def create_result(match, type, as_user):
    with open(BaseTestCase.test_replay_path, 'rb') as result_replay:
        result = Result.objects.create(match=match, type=type, replay_file=File(result_replay), game_steps=1,
                                       submitted_by=as_user)
        result.finalize_submission(None, None, None, None, 0.111111, 0.222222)


def run_seed(rounds, token):
    devadmin = User.objects.create_superuser(username='devadmin', password='x', email='devadmin@aiarena.net')

    arenaclient = User.objects.create_user(username='aiarenaclient-000', password='x',
                                           email='aiarenaclient-000@aiarena.net', is_staff=True, service_account=True)

    # if token is None it will generate a new one, otherwise it will use the one specified
    new_token = Token.objects.create(user=arenaclient, key=token)

    devuser1 = User.objects.create_user(username='devuser1', password='x', email='devuser1@aiarena.net')
    devuser2 = User.objects.create_user(username='devuser2', password='x', email='devuser2@aiarena.net')

    with open(BaseTestCase.test_map_path, 'rb') as map:
        Map.objects.create(name='test_map', file=File(map))

    with open(BaseTestCase.test_bot_zip_path, 'rb') as bot_zip:
        Bot.objects.create(user=devadmin, name='devadmin_bot1', active=True, plays_race='T', type='python',
                           bot_zip=File(bot_zip))
        Bot.objects.create(user=devadmin, name='devadmin_bot2', active=True, plays_race='Z', type='python',
                           bot_zip=File(bot_zip))
        Bot.objects.create(user=devadmin, name='devadmin_bot3', plays_race='P', type='python',
                           bot_zip=File(bot_zip))  # inactive bot

        Bot.objects.create(user=devuser1, name='devuser1_bot1', active=True, plays_race='P', type='python',
                           bot_zip=File(bot_zip))
        Bot.objects.create(user=devuser1, name='devuser1_bot2', active=True, plays_race='Z', type='python',
                           bot_zip=File(bot_zip))
        Bot.objects.create(user=devuser1, name='devuser1_bot3', plays_race='T', type='python',
                           bot_zip=File(bot_zip))  # inactive bot

        Bot.objects.create(user=devuser2, name='devuser2_bot1', active=True, plays_race='P', type='python',
                           bot_zip=File(bot_zip))
        Bot.objects.create(user=devuser2, name='devuser2_bot2', active=True, plays_race='T', type='python',
                           bot_zip=File(bot_zip))
        Bot.objects.create(user=devuser2, name='devuser2_bot3', plays_race='Z', type='python',
                           bot_zip=File(bot_zip))  # inactive bot

    for x in range(rounds - 1):  # 4 active bots - 6 games per round
        match = create_match(devadmin)
        create_result(match, 'Player1Win', devadmin)
        match = create_match(devadmin)
        create_result(match, 'Player2Win', devadmin)
        match = create_match(devadmin)
        create_result_with_bot_data_and_logs(match, 'Player1Crash', devadmin)
        match = create_match(devadmin)
        create_result(match, 'Player1TimeOut', devadmin)
        match = create_match(devadmin)
        create_result_with_bot_data_and_logs(match, 'Tie', devadmin)
        match = create_match(devadmin)
        create_result(match, 'Timeout', devadmin)

    # one last to tick over into the final round so we don't have an empty match queue
    create_match(devadmin)

    return new_token


class Command(BaseCommand):
    help = "Seed database for testing and development."

    _DEFAULT_ROUNDS_TO_GENERATE = 10

    def add_arguments(self, parser):
        parser.add_argument('--rounds', type=int, help="Number of rounds to generate. Default is {0}.".format(
            self._DEFAULT_ROUNDS_TO_GENERATE))
        parser.add_argument('--token', type=str,
                            help="Specify the token to use for the arena client."
                                 " Useful to avoid having to reconfigure arena clients in testing".format(
                                self._DEFAULT_ROUNDS_TO_GENERATE))

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        if settings.ENVIRONMENT_TYPE == EnvironmentType.DEVELOPMENT \
                or settings.ENVIRONMENT_TYPE == EnvironmentType.STAGING:
            if options['rounds'] is not None:
                rounds = options['rounds']
            else:
                rounds = self._DEFAULT_ROUNDS_TO_GENERATE

            if options['token'] is not None:
                token = options['token']
            else:
                token = None

            self.stdout.write('Generating {0} round(s)...'.format(rounds))
            api_token = run_seed(rounds, token)

            self.stdout.write('Done. User logins have a password of "x".')
            self.stdout.write('API Token is {0}.'.format(api_token))
        else:
            self.stdout.write('Seeding failed: This is not a development or staging environment!')
