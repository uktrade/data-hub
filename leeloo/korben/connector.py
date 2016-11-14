"""Talk to Korben API for saving."""


from django.conf import settings

import requests
from django.core.serializers.json import DjangoJSONEncoder

from .utils import generate_signature


class KorbenConnector:

    default_headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
    }

    def encode_json_bytes(self, model_dict):
        json_str = self._json_encoder.encode(model_dict)
        return bytes(json_str, 'utf-8')

    def __init__(self, table_name):
        self._json_encoder = DjangoJSONEncoder()
        self.table_name = table_name
        self.base_url = 'http://{host}:{port}'.format(
            host=settings.KORBEN_HOST, port=settings.KORBEN_PORT
        )

    def inject_auth_header(self, url, body):
        self.default_headers['X-Signature'] = generate_signature(url, body, settings.DATAHUB_SECRET)

    def post(self, data, update=False):
        """Perform POST operations: create and update.

        :param data: dict object containing the data to be passed to Korben
        :param update: whether the POST request has to be treated as an UPDATE
        :return: requests Response object
        """
        if update:
            url = '{base_url}/update/{table_name}/'.format(
                base_url=self.base_url,
                table_name=self.table_name
            )
        else:
            url = '{base_url}/create/{table_name}/'.format(
                base_url=self.base_url,
                table_name=self.table_name
            )

        data = self.encode_json_bytes(data)
        self.inject_auth_header(url, data)
        response = requests.post(url=url, data=data, headers=self.default_headers)
        return response

    def get(self, data):
        """Get single object from Korben.

        :param object_id: object id
        :return: requests Response object
        """
        url = '{base_url}/get/{table_name}/{id}/'.format(
            base_url=self.base_url,
            table_name=self.table_name,
            id=data['id']
        )
        data = self.encode_json_bytes(data)
        self.inject_auth_header(url, data)
        response = requests.post(url=url, data=data, headers=self.default_headers)
        return response
