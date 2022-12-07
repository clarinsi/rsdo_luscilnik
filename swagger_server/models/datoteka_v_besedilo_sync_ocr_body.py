# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class DatotekaVBesediloSyncOcrBody(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, file: str=None):  # noqa: E501
        """DatotekaVBesediloSyncOcrBody - a model defined in Swagger

        :param file: The file of this DatotekaVBesediloSyncOcrBody.  # noqa: E501
        :type file: str
        """
        self.swagger_types = {
            'file': str
        }

        self.attribute_map = {
            'file': 'file'
        }
        self._file = file

    @classmethod
    def from_dict(cls, dikt) -> 'DatotekaVBesediloSyncOcrBody':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The datotekaVBesediloSync_ocr_body of this DatotekaVBesediloSyncOcrBody.  # noqa: E501
        :rtype: DatotekaVBesediloSyncOcrBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def file(self) -> str:
        """Gets the file of this DatotekaVBesediloSyncOcrBody.


        :return: The file of this DatotekaVBesediloSyncOcrBody.
        :rtype: str
        """
        return self._file

    @file.setter
    def file(self, file: str):
        """Sets the file of this DatotekaVBesediloSyncOcrBody.


        :param file: The file of this DatotekaVBesediloSyncOcrBody.
        :type file: str
        """
        if file is None:
            raise ValueError("Invalid value for `file`, must not be `None`")  # noqa: E501

        self._file = file
