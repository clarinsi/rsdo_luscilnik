# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.izlusci_body import IzlusciBody  # noqa: E501
from swagger_server.models.terminoloski_kandidat import TerminoloskiKandidat  # noqa: E501
from swagger_server.test import BaseTestCase


class TestExtractController(BaseTestCase):
    """ExtractController integration test stubs"""

    def test_get_candidates(self):
        """Test case for get_candidates

        Izlusci terminološke kandidate iz seznama besedil v conllu obliki
        """
        body = IzlusciBody()
        response = self.client.open(
            '/izlusci',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
