import os.path

import pytesseract
import requests
import docx
import xml.etree.ElementTree as ET
from PyPDF2 import PdfReader
from swagger_server.utils import cl_utils
import cv2
import numpy as np
import magic

tika_server = "http://tika2:9999/tika"


# endpoint below to be used only for development purposes (don't need to run docker)
# tika_server = "http://rsdo.lhrs.feri.um.si:9998/tika"

def extract_text_prepResp(file, content_type=""):
    content_type = file.content_type
    if content_type is None:
        content_type = magic.from_file(file.stream.name, mime=True)

    if tika_responding():
        response = requests.put(tika_server, data=file, headers={"Accept": "text/plain; charset=UTF-8"})
        return response.text, 200
    if "openxmlformats-officedocument.wordprocessingml.document" in content_type:
        content = '\n'.join([p.text for p in docx.Document(file).paragraphs])
    elif "application/pdf" in content_type:
        reader = PdfReader(file)
        content = '\n'.join([p.extract_text() for p in reader.pages])
        content = content
    elif "text/xml" in content_type:
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
                                headers={"X-Tika-PDFOcrStrategy": "ocr_only", "X-Tika-OCRLanguage": "slv+eng","Accept": "text/plain; charset=UTF-8"})
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