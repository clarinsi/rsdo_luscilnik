from swagger_server.utils import cl_utils
from swagger_server.utils import txt_utils


def datoteka_v_besedilo_in_classla(file=None):  # noqa: E501
    """Pretvori datoteko formata pdf, doc, docx, ppt, xls,... vrača conllu

     # noqa: E501

    :param file:
    :type file: strstr

    :rtype: str
    """
    if not cl_utils.nlp_loaded:
        return "NLP Models still loading up since server restart, please try again later.", 500
    if file is None:
        return "No file provided", 400
    try:
        txt, _ = txt_utils.extract_text_prepResp(file)
        return cl_utils.raw_text_to_conllu(txt)
    except Exception as e:
        return str(e), 500


def datoteka_v_besedilo_sync_post(file=None):  # noqa: E501
    """Pretvori datoteko formata pdf, doc, docx, ppt, xls,... vrača besedilo

     # noqa: E501

    :param file:
    :type file: strstr

    :rtype: str
    """
    if file is None:
        return "No file provided", 400
    try:
        return txt_utils.extract_text_prepResp(file)
    except Exception as e:
        print(e)
        return str(e), 500


def get_conllu_ocr(file=None):  # noqa: E501
    """Pretvori datoteko formata pdf, doc, docx, ppt, xls,... v conllu s pomočjo ocr razpoznavanja

     # noqa: E501

    :param file:
    :type file: strstr

    :rtype: str
    """
    if not cl_utils.nlp_loaded:
        return "NLP Models still loading up since server restart, please try again later.", 500
    if file is None:
        return "No file provided", 400
    try:
        txt, _ = txt_utils.ocr_text_prepResp(file)
        return cl_utils.raw_text_to_conllu(txt)
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
        return txt_utils.ocr_text_prepResp(file)
    except Exception as e:
        return str(e), 500
