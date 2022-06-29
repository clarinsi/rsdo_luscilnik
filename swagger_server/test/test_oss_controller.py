# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.terminoloski_kandidat import TerminoloskiKandidat  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOssController(BaseTestCase):
    """OssController integration test stubs"""

    def test_get_conllu(self):
        """Test case for get_conllu

        Vrne CoNNL-U po id-ju datoteke
        """
        query_string = [('file_id', 789)]
        response = self.client.open(
            '/oss/conlluPoId',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_conllus(self):
        """Test case for get_conllus

        Vrne seznam CoNNL-U-jev glede na iskalne pogoje
        """
        query_string = [('leta', 56),
                        ('vrste', 'vrste_example'),
                        ('kljucnebesede', 'kljucnebesede_example'),
                        ('cerifpodrocja', 56)]
        response = self.client.open(
            '/oss/conlluPoIskanju',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_extracted_words(self):
        """Test case for get_extracted_words

        Vrne terminloške kandidate glede na 
        """
        query_string = [('leta', 56),
                        ('vrste', 'vrste_example'),
                        ('kljucnebesede', 'kljucnebesede_example'),
                        ('cerifpodrocja', 56)]
        response = self.client.open(
            '/oss/izlusciPoIskanju',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_file(self):
        """Test case for get_file

        Vrne binarni zapis v originalnem formatu po id-ju datoteke
        """
        query_string = [('file_id', 789)]
        response = self.client.open(
            '/oss/datotekaPoId',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_files(self):
        """Test case for get_files

        Vrne seznam binarnih zapisov v originalnem formatu glede na iskalne pogoje
        """
        query_string = [('leta', 56),
                        ('vrste', 'vrste_example'),
                        ('kljucnebesede', 'kljucnebesede_example'),
                        ('cerifpodrocja', 56)]
        response = self.client.open(
            '/oss/datotekePoIskanju',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_number_texts(self):
        """Test case for get_number_texts

        Vrne število besedil glede na iskalne pogoje
        """
        query_string = [('leta', 56),
                        ('vrste', 'vrste_example'),
                        ('kljucnebesede', 'kljucnebesede_example'),
                        ('cerifpodrocja', 56)]
        response = self.client.open(
            '/oss/steviloBesedilPoIskanju',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_texts(self):
        """Test case for get_texts

        Vrne seznam besedil glede na iskalne pogoje
        """
        query_string = [('leta', 56),
                        ('vrste', 'vrste_example'),
                        ('kljucnebesede', 'kljucnebesede_example'),
                        ('cerifpodrocja', 56)]
        response = self.client.open(
            '/oss/besedilaPoIskanju',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_oss_besedilo_po_id_get(self):
        """Test case for oss_besedilo_po_id_get

        Vrne besedilo po id-ju datoteke
        """
        query_string = [('file_id', 789)]
        response = self.client.open(
            '/oss/besediloPoId',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
