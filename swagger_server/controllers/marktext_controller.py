import connexion
import six

from swagger_server.models.oznaci_besedilo_body import OznaciBesediloBody  # noqa: E501
from swagger_server import util
from swagger_server.classla import cl_utils
from swagger_server.requets_db.models.vrsta import (Job, JobManager)


def get_text(body):  # noqa: E501
    """Označi besedilo s classlo/stanzo z uporabo slovenskih modelov ter vrne conll-u format

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = OznaciBesediloBody.from_dict(connexion.request.get_json())  # noqa: E501
    # conllu = cl_utils.raw_text_to_conllu(body.besedilo)
    # return conllu
    job, is_old_job = JobManager.create_job(1, body.besedilo)
    if job is None:
        return "Something went wrong", 500
    ret = {'check_job_url': f'{connexion.request.url_root}/job/{job.id}'}

    return ret  # Todo: Update swagger to the newest response template later
