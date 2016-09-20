"""Search views."""

from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from core.utils import get_elasticsearch_client, format_es_results

from .utils import search_by_term


class Search(APIView):
    """This endpoint handles the search."""

    http_method_names = ('post', )

    def post(self, request, format=None):
        """Search is a POST."""
        try:
            query_term = request.data['term']
        except MultiValueDictKeyError:
            raise ValidationError(detail=['Parameter "term" is mandatory.'])
        offset = request.data.get('offset', 0)
        limit = request.data.get('limit', 100)
        client = get_elasticsearch_client()
        results = search_by_term(
            client=client,
            index=settings.ES_INDEX,
            term=query_term,
            offset=int(offset),
            limit=int(limit)
        )
        formatted_results = format_es_results(results.hits.hits)
        return Response(data=formatted_results)
