import os.path
from tempfile import TemporaryFile

import connexion
import pytesseract
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
import traceback
import cv2
import numpy as np

tika_server = "http://tika2:9999/tika_NAROBENURLZANALASC"


# endpoint below to be used only for development purposes (don't need to run docker)
# tika_server = "http://rsdo.lhrs.feri.um.si:9998/tika"


def extract_text_prepResp(file):
    if tika_responding():
        response = requests.put(tika_server, data=file)
        return response.text, 200
    if "openxmlformats-officedocument.wordprocessingml.document" in file.content_type:
        content = [p.text for p in docx.Document(file).paragraphs]
    elif "application/pdf" in file.content_type:
        reader = PdfReader(file)
        content = '\n'.join([p.extract_text() for p in reader.pages])
        content = "ZACASNO UPORABLJEN DRUGI BRALEC KOT TIKA, TA BO SE DODANA KASNEJE...\n\n" + content
    elif "text/xml" in file.content_type:
        root = ET.parse(file).getroot()
        plainText = root.findall('PlainText')
        if len(plainText) == 0:
            return "Didn't find anything in PlainText", 400
        content = '\n'.join([pt.text for pt in plainText])
    # elif "text/plain" in file.content_type:
    else:
        content = file.read().decode('utf-8')

    return content, 200


def ocr_text_prepResp(file):
    if tika_responding():
        response = requests.put(tika_server, data=file,
                                headers={"X-Tika-PDFOcrStrategy": "ocr_only", "X-Tika-OCRLanguage": "slv+eng"})
        return response.text, 200

    win_p = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    if os.path.exists(win_p):
        pytesseract.pytesseract.tesseract_cmd = win_p

    # convert string data to numpy array
    file_bytes = np.fromstring(file.read(), np.uint8)
    # convert numpy array to image
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    conf = '-l eng+slv'
    return pytesseract.image_to_string(img, config=conf), 200


def tika_responding():
    try:
        ret = requests.get(tika_server)
        return ret.status_code == 200
    except:
        return False


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
        return extract_text_prepResp(file)
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
        return ocr_text_prepResp(file)
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
        txt, _ = extract_text_prepResp(file)
        return cl_utils.raw_text_to_conllu(txt)
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
        if tika_responding():
            response = requests.put(tika_server, data=file,
                                    headers={"X-Tika-PDFOcrStrategy": "ocr_only", "X-Tika-OCRLanguage": "slv+eng"})
            return cl_utils.raw_text_to_conllu(response.text)
        else:
            txt, _ = ocr_text_prepResp(file)
            return cl_utils.raw_text_to_conllu(txt)
    except Exception as e:
        return str(e), 500
