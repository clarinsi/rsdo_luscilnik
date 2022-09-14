import connexion

from swagger_server.models.oznaci_besedilo_async_body import OznaciBesediloAsyncBody  # noqa: E501
from swagger_server.requets_db.models.vrsta import (JobManager)
from swagger_server.utils import txt_utils


def get_text(body):  # noqa: E501
    """Označi besedilo s classlo/stanzo z uporabo slovenskih modelov ter vrne conll-u format

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = OznaciBesediloAsyncBody.from_dict(connexion.request.get_json())  # noqa: E501
    # conllu = cl_utils.raw_text_to_conllu(body.besedilo)
    # return conllu
    job, is_old_job = JobManager.create_job(2, body.besedilo)
    if job is None:
        return "Something went wrong", 500
    ret = {'check_job_url': f'{connexion.request.url_root}/job/{job.id}'}

    return ret, 200  # Todo: Update swagger to the newest response template later


def get_conllu_from_file_async(file=None):  # noqa: E501
    """Pretvori datoteko v besedilo in označi s classlo/stanzo z uporabo slovenskih modelov ter vrne conll-u format

     # noqa: E501

    :param file:
    :type file: strstr

    :rtype: str
    """
    return 'do some magic!'


def get_conllu_from_file_ocr_async(file=None):  # noqa: E501
    """Pretvori datoteko v besedilo in označi s classlo/stanzo z uporabo slovenskih modelov ter vrne conll-u format

     # noqa: E501

    :param file:
    :type file: strstr

    :rtype: str
    """
    return 'do some magic!'


def get_text_from_doc_async(file=None):  # noqa: E501
    """Pretvori datoteko v besedilo, vrača tekst

     # noqa: E501

    :param file:
    :type file: strstr

    :rtype: str
    """
    return 'do some magic!'


def get_text_from_file_ocr_async(file=None):  # noqa: E501
    """Pretvori datoteko v besedilo s pomočjo ocr razpoznavanja, vrača tekst

     # noqa: E501

    :param file:
    :type file: strstr

    :rtype: str
    """
    return 'do some magic!'
