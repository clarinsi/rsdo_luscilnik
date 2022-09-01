# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.oznaci_besedilo_async_body import OznaciBesediloAsyncBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMarktextController(BaseTestCase):
    """MarktextController integration test stubs"""

    def test_get_text(self):
        """Test case for get_text

        Označi besedilo s classlo/stanzo z uporabo slovenskih modelov ter vrne conll-u format
        """
        body = OznaciBesediloAsyncBody()
        response = self.client.open(
            '/oznaciBesediloAsync',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
