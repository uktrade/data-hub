from django.urls import reverse
from rest_framework import status

from core.test_utils import LeelooTestCase
from .factories import AdvisorFactory


class AdvisorTestCase(LeelooTestCase):

    def test_advisor_list_view(self):
        """Should return id and name."""

        AdvisorFactory()
        url = reverse('advisor-list')
        response = self.api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
