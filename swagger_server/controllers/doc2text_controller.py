from tempfile import TemporaryFile

import connexion
import six
import requests
import json
from swagger_server import util
import pandas as pd
import docx
import codecs
import xml.etree.ElementTree as ET
from PyPDF2 import PdfReader
from swagger_server.classla import cl_utils

tika_server = "http://tika:9998/tika"

# endpoint below to be used only for development purposes (don't need to run docker)
# tika_server = "http://rsdo.lhrs.feri.um.si:9998/tika"


def datoteka_v_besedilo_post(file=None):  # noqa: E501
    """Pretvori datoteko formata pdf, doc, docx, ppt, xls,... vraca besedilo

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


def get_text_ocr(file=None):  # noqa: E501
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


def datoteka_v_besedilo_in_classla(file=None):  # noqa: E501
    """Pretvori datoteko formata pdf, doc, docx, ppt, xls,... vraca conllu

     # noqa: E501

    :param file:
    :type file: strstr

    :rtype: str
    """
    if not cl_utils.nlp_loaded:
        return "NLP Models still loading up since server restart, please retry later.", 500
    if file is None:
        return "No file provided", 400
    try:
        response = requests.put(tika_server, data=file)
        return cl_utils.raw_text_to_conllu(response.text)
    except Exception as e:
        return str(e), 500


def get_conllu_ocr(file=None):  # noqa: E501
    """Pretvori datoteko formata pdf, doc, docx, ppt, xls,... v conllu s pomočjo ocr razpoznavanja

     # noqa: E501

    :param file:
    :type file: strstr

    :rtype: str
    """
    if not cl_utils.nlp_loaded:
        return "NLP Models still loading up since server restart, please retry later.", 500
    if file is None:
        return "No file provided", 400
    try:
        response = requests.put(tika_server, data=file,
                                headers={"X-Tika-PDFOcrStrategy": "ocr_only", "X-Tika-OCRLanguage": "slv+eng"})
        return cl_utils.raw_text_to_conllu(response.text)
    except Exception as e:
        return str(e), 500
