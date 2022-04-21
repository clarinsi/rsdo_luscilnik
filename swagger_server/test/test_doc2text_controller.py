# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestDoc2textController(BaseTestCase):
    """Doc2textController integration test stubs"""

    def test_datoteka_v_besedilo_post(self):
        """Test case for datoteka_v_besedilo_post

        Pretvori datoteko formata pdf, doc, docx, ppt, xls,... v besedilo
        """
        data = dict(file='file_example')
        response = self.client.open(
            '/datotekaVBesedilo/',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_text_ocr(self):
        """Test case for get_text_ocr

        Pretvori datoteko formata pdf, doc, docx, ppt, xls,... v besedilo s pomočjo ocr razpoznavanja
        """
        data = dict(file='file_example')
        response = self.client.open(
            '/datotekaVBesedilo/ocr',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
