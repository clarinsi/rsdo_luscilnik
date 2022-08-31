from tempfile import TemporaryFile

import connexion
import six
# import tika
import requests
import json
from swagger_server import util
import pandas as pd
import docx
import codecs
import xml.etree.ElementTree as ET
from PyPDF2 import PdfReader

tika_server = "http://tika:9998/tika"


tika_server = "http://rsdo.lhrs.feri.um.si:9998/tika"


def datoteka_v_besedilo_post(file=None):  # noqa: E501
    """Pretvori datoteko formata pdf, doc, docx, ppt, xls,... v besedilo

     # noqa: E501

    :param file: 
    :type file: strstr

    :rtype: str
    """
    if file is None:
        return "No file provided", 400
    try:
        response = requests.put(tika_server, data=file)
        return response.text, 200
    except Exception as e:
        return str(e), 500


def get_text_ocr(file=None):
    """Pretvori datoteko formata pdf, doc, docx, ppt, xls,... v besedilo s pomočjo ocr razpoznavanja


     # noqa: E501

    :param file:
    :type file: strstr

    :rtype: str
    """

    if file is None:
        return "No file provided", 400
    try:
        response = requests.put(tika_server, data=file,
                                 headers={"X-Tika-PDFOcrStrategy": "ocr_only", "X-Tika-OCRLanguage": "slv+eng"})
        return response.text, 200
    except Exception as e:
        return str(e), 500

