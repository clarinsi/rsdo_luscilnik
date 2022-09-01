import connexion
import six

from swagger_server.models.oznaci_besedilo_async_body import OznaciBesediloAsyncBody  # noqa: E501
from swagger_server import util
from swagger_server.classla import cl_utils
from swagger_server.requets_db.models.vrsta import (Job, JobManager)
import swagger_server.controllers.doc2text_controller as d2t


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
    job, is_old_job = JobManager.create_job(1, body.besedilo)
    if job is None:
        return "Something went wrong", 500
    ret = {'check_job_url': f'{connexion.request.url_root}/job/{job.id}'}

    return ret, 200  # Todo: Update swagger to the newest response template later


def get_text_from_file(file=None):  # noqa: E501
    """Pretvori datoteko v besedilo in označi s classlo/stanzo z uporabo slovenskih modelov ter vrne conll-u format

     # noqa: E501

    :param file:
    :type file: strstr

    :rtype: str
    """
    if file is None:
        return "No file provided", 400
    txt, status = d2t.extract_text_prepResp(file)
    # Todo: instead of parsing text here, instead save the file into the tb or locally, and then parsing
    # Todo: when the job actually executes (this version of the implementation is temporary)

    if status == 200:
        job, is_old_job = JobManager.create_job(1, txt)
        if job is None:
            return "Something went wrong", 500
        ret = {'check_job_url': f'{connexion.request.url_root}/job/{job.id}'}
        return ret, 200
    else:
        return "Something went wrong", 500


def get_text_from_file_ocr(file=None):  # noqa: E501
    """Pretvori datoteko v besedilo s pomočjo ocr razpoznavanja in označi s classlo/stanzo z uporabo slovenskih modelov ter vrne conll-u format

     # noqa: E501

    :param file:
    :type file: strstr

    :rtype: str
    """
    if file is None:
        return "No file provided", 400
    txt, status = d2t.ocr_text_prepResp(file)
    # Todo: instead of ocr-ing text here, instead save the file into the tb or locally, and then ocr
    # Todo: when the job actually executes (this version of the implementation is temporary)

    if status == 200:
        job, is_old_job = JobManager.create_job(1, txt)
        if job is None:
            return "Something went wrong", 500
        ret = {'check_job_url': f'{connexion.request.url_root}/job/{job.id}'}
        return ret, 200
    else:
        return "Something went wrong", 500
