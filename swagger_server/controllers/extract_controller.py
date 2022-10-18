import codecs
import os

import connexion
import json
from pathlib import Path
from swagger_server.models.izlusci_async_body import IzlusciAsyncBody  # noqa: E501
from swagger_server.models.izlusci_sync_body import IzlusciSyncBody  # noqa: E501
from swagger_server.requets_db.models.vrsta import JobManager
from swagger_server.utils import cl_utils
from swagger_server.util import get_random_filename, create_random_file_in_tmp_folder
import requests
from werkzeug.utils import secure_filename

# ATEapi_endpoint = "http://localhost:5000/predict"


ATEapi_endpoint = "http://ate-api:5000/predict"


def do_izlusci(conllus, prepovedane_besede):
    tmp_file_path = ""
    try:
        big_conllu = cl_utils.multipla_conllus_to_one_from_conllus_arr(conllus)
        tmp_file_path = create_random_file_in_tmp_folder(big_conllu, ".conllu")
        fp = open(tmp_file_path, 'rb')
        try:
            files = [
                ('file', ('temp_1.conllu', fp, 'application/octet-stream'))
            ]
            res = requests.post(ATEapi_endpoint, files=files)
            data = json.loads(res.text)
        finally:
            fp.close()
            os.remove(tmp_file_path)

        ret = {'terminoloski_kandidati': [
            {
                'POSoznake': tk['msd'],
                'kandidat': tk['terms'],  # more to bit lemma al terms?
                'kanonicnaoblika': tk['canonical'],
                'ranking': tk['ranking'],
                'podporneutezi': [
                    0.0,  # ????????
                    0.0  # ??????
                ],
                'pogostostpojavljanja': [0, 0]  # ???????
            }
            for tk in data if tk['terms'] not in prepovedane_besede
        ]}
        return ret, 200
    except Exception as e:
        return str(e), 500


def get_candidates_async(body):  # noqa: E501
    """Izlusci terminološke kandidate iz seznama besedil v conllu obliki [asinhrono, ustvari novi job]

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = IzlusciAsyncBody.from_dict(connexion.request.get_json())  # noqa: E501
    job, is_old_job = JobManager.create_job(4, json.dumps(body.to_dict()))
    if job is None:
        return "Something went wrong", 500
    ret = {'check_job_url': f'{connexion.request.url_root}/job/{job.id}'}
    return ret, 200


def get_candidates_sync(body):  # noqa: E501
    """Izlusci terminološke kandidate iz seznama besedil v conllu obliki [sihrono, rezultat v sami zahtevi]

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: List[TerminoloskiKandidat]
    """
    if connexion.request.is_json:
        body = IzlusciSyncBody.from_dict(connexion.request.get_json())  # noqa: E501

    return do_izlusci(body.conllus, body.prepovedane_besede)
