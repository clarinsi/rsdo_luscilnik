import connexion
import six
# import tika

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

    if file is None:
        return "No file provided", 400
    elif "openxmlformats-officedocument.wordprocessingml.document" in file.content_type:
        content = [p.text for p in docx.Document(file).paragraphs]
    elif "text/plain" in file.content_type:
        content = file.read().decode('utf-8')
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
    else:
        return "Currently supporing only docx, txt/plain, pdf, xml*... more will be added later", 501

    return content, 200


def get_text_ocr(file=None):  # noqa: E501
    """Pretvori datoteko formata pdf, doc, docx, ppt, xls,... v besedilo s pomočjo ocr razpoznavanja

     # noqa: E501

    :param file: 
    :type file: strstr

    :rtype: str
    """
    return 'Not yet implemented'
