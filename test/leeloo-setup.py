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
client_secret = os.environ['API_CLIENT_SECRET']
client_id = os.environ['API_CLIENT_ID']

try:
    test_user = Advisor.objects.get(email=username)
except Advisor.DoesNotExist:
    test_user = Advisor(
        email=username,
    )

test_user.first_name = 'Test'
test_user.last_name = 'User'
test_user.set_password(password)
test_user.is_superuser = True
test_user.is_staff = True
test_user.is_active = True
test_user.dit_team = Team.objects.get(name='London International Trade Team')
test_user.save(as_korben=True)

APPLICATION_NAME = 'Browser tests'
try:
    app = Application.objects.get(name=APPLICATION_NAME)
except Application.DoesNotExist:
    app = Application()

app.user = test_user
app.client_type = Application.CLIENT_CONFIDENTIAL
app.client_id = client_id
app.client_secret = client_secret
app.authorization_grant_type = Application.GRANT_PASSWORD
app.name = APPLICATION_NAME
app.save()
