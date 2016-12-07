import os

import sys
sys.path.append(os.getcwd())

import django
django.setup()
from datahub.company.models import Advisor
from datahub.metadata.models import Team

username = os.environ['TEST_LEELOO_SUPERUSER_USERNAME']
password = os.environ['TEST_LEELOO_SUPERUSER_PASSWORD']

try:
    test_user = Advisor.objects.get(email=username)
except Advisor.DoesNotExist:
    test_user = Advisor(email=username)
    test_user.set_password(password)
    test_user.is_superuser = True
    test_user.is_staff = True
    test_user.save()
test_user.advisor.dit_team = Team.objects.get(name='London International Trade Team')
test_user.advisor.save()
