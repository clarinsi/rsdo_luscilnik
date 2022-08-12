# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.job_response import JobResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestJobsController(BaseTestCase):
    """JobsController integration test stubs"""

    def test_get_job_status(self):
        """Test case for get_job_status

        Vrne status
        """
        query_string = [('job_id', 789),
                        ('show_estimated_completion', True)]
        response = self.client.open(
            '/job',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
