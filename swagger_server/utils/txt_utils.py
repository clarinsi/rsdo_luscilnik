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
import re
#to še mora v env 
tika_server = "http://tika2:9999/tika"

# endpoint below to be used only for development purposes (don't need to run docker)
# tika_server = "http://rsdo.lhrs.feri.um.si:9998/tika"


def extract_text_prepResp(file, content_type=""):
    content_type = file.content_type
    if content_type is None:
        content_type = magic.from_file(file.stream.name, mime=True)

    content = ""
    if tika_responding():
        try:
            response = requests.put(tika_server, data=file, headers={"Accept": "text/plain; charset=UTF-8"})
            content = response.text
            #preveri če je pretvorba uspešna
            
            # original string
            res = re.findall(r'\w+', content)

            #preveri, če imamo vsaj 10 besed in če je povprečna dolžina >3 in < 12
            #če to drži, idi v ocr
            reslen=map(lambda n:len(n),res)
            print(f"Število besed je {len(res)}")

            if len(res)>0 :
                avglen=sum(reslen)/len(res)
            else:
                avglen=0
            
            print(f"Povprečna dolžina besede je {avglen}")
            
            if(len(res)<10 or avglen<4 or avglen>11):
                print("Besedilo je sumljivo, gremo v OCR in damo file na začetek!")
                file.seek(0)
                response = requests.put(tika_server, data=file, headers={"X-Tika-PDFOcrStrategy": "ocr_only", "X-Tika-OCRLanguage": "slv+eng",
                                             "Accept": "text/plain; charset=UTF-8"})
                content = response.text

            #odstranim še vse prelome vrstic, ker imamo s tem probleme
            content=' '.join(content.splitlines())
        except:
            content = "ERROR - something went wrong when reading file with tika"

    #if content == "":
    #    if "openxmlformats-officedocument.wordprocessingml.document" in content_type:
    #        content = '\n'.join([p.text for p in docx.Document(file).paragraphs])
    #    elif "application/pdf" in content_type:
    #        reader = PdfReader(file)
    #        content = '\n'.join([p.extract_text() for p in reader.pages])
    #       content = content
    #    elif "text/xml" in content_type:
    #        root = ET.parse(file).getroot()
    #        plainText = root.findall('PlainText')
    #        if len(plainText) == 0:
    #            return "Didn't find anything in PlainText", 400
    #        content = '\n'.join([pt.text for pt in plainText])
    #   # elif "text/plain" in file.content_type:
    #    else:
    #       try:
    #           content = file.read().decode('utf-8')
    #       except:
    #           content = "ERROR - something went wrong when reading file with not-tika method!"

    return content, 200


def ocr_text_prepResp(file):
    content = ""
    if tika_responding():
        try:
            response = requests.put(tika_server, data=file,
                                    headers={"X-Tika-PDFOcrStrategy": "ocr_only", "X-Tika-OCRLanguage": "slv+eng",
                                             "Accept": "text/plain; charset=UTF-8"})
            content = response.text
        except:
            content = "ERROR - something went wrong when reading file with tika (OCR)"

    if content == "":
        try:
            win_p = "C:/Program Files/Tesseract-OCR/tesseract.exe"
            if os.path.exists(win_p):
                pytesseract.pytesseract.tesseract_cmd = win_p

            # convert string data to numpy array
            file_bytes = np.fromstring(file.read(), np.uint8)
            # convert numpy array to image
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            conf = '-l eng+slv'
            content = pytesseract.image_to_string(img, config=conf)
        except:
            content = "ERROR - something went wrong when reading file with not-tika method! (OCR)"

    return content, 200


def tika_responding():
    try:
        ret = requests.get(tika_server)
        return ret.status_code == 200
    except:
        return False
