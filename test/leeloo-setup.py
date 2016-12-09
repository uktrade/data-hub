import os

import sys
sys.path.append(os.getcwd())

import django
django.setup()
from datahub.company.models import Advisor
from datahub.metadata.models import Team

from oauth2_provider.models import AccessToken, Application, Grant, RefreshToken

username = os.environ['CDMS_USERNAME']
password = os.environ['CDMS_PASSWORD']

try:
    test_user = Advisor.objects.get(email=username)
except Advisor.DoesNotExist:
    test_user = Advisor(
        first_name='Test',
        last_name='User',
        email=username,
    )
test_user.set_password(password)
test_user.is_superuser = True
test_user.is_staff = True
test_user.dit_team = Team.objects.get(name='London International Trade Team')
test_user.save(as_korben=True)

APPLICATION_NAME = 'Browser tests'
try:
    app = Application.objects.get(name=APPLICATION_NAME)
except Application.DoesNotExist:
    app = Application(
        user=test_user,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD,
        name=APPLICATION_NAME,
    )
    app.save()


if len(sys.argv) > 1:
    print("API_ROOT={0}".format('http://leeloo:8000'))
    print("REDIS_HOST={0}".format('redis-rhod'))
    print("REDIS_PORT={0}".format('6379'))
    print("REDIS_URL={0}".format('redis://:@redis-rhod:6379'))
    print("API_CLIENT_ID={0}".format(app.client_id))
    print("API_CLIENT_SECRET={0}".format(app.client_secret))
    print("SESSION_SECRET={0}".format('abc123'))
