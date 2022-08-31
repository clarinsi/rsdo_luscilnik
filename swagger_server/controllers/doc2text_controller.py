import connexion
import six
# import tika
import requests

from swagger_server import util
import pandas as pd
import docx
import codecs
import xml.etree.ElementTree as ET
from PyPDF2 import PdfReader


def datoteka_v_besedilo_post(file=None):  # noqa: E501
    """Pretvori datoteko formata pdf, doc, docx, ppt, xls,... v besedilo

     # noqa: E501

    :param file: 
    :type file: strstr

    :rtype: str
    """
    #zakaj ? tika server se požene zraven v dodatnem containerju in se datoteka samo pošlje tja, nazaj pa se dobi čisto besedilo...
    #tika ima rest api
    if file is None:
        return "No file provided", 400

    tika_server="http://tika:9998/tika"
    response=requests.post(tika_server, data=file)
    return response.text, 200


def get_text_ocr(file=None):  # noqa: E501
    

    if file is None:
        return "No file provided", 400

    tika_server="http://tika:9998/tika"
    #za ocr se zraven samo doda header 
    response=requests.post(tika_server, data=file,headers={"X-Tika-PDFOcrStrategy":"ocr_only","X-Tika-OCRLanguage":"slv+eng"})
    return response.text, 200


