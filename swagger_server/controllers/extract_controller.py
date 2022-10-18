import connexion
import json
from pathlib import Path
from swagger_server.models.izlusci_body import IzlusciBody  # noqa: E501
from swagger_server.classla import cl_utils
import requests

# ATEapi_endpoint = "http://localhost:5000/predict"


ATEapi_endpoint = "http://ate-api:5000/predict"


def get_candidates(body):  # noqa: E501
    """Izlusci terminološke kandidate iz seznama besedil v conllu obliki

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: List[TerminoloskiKandidat]
    """
    if connexion.request.is_json:
        body = IzlusciBody.from_dict(connexion.request.get_json())  # noqa: E501

    # Todo: What is "conllus" in body input anyway??
    # Todo: Kaj je s prepovedanimi besedami?
    # file_ids = [10000, 10001, 10002, 10003]
    # big_conllu = cl_utils.multipla_conllus_to_one_from_file_ids(file_ids)

    # txt = Path('../ATEapi/temp_1.conllu').read_text('utf-8')  # LOCAL ONLY

    # # Todo: does this close the file after the request?
    # files = [
    #     ('file', ('temp_1.conllu', open('../ATEapi/temp_1.conllu', 'rb'),
    #               'application/octet-stream'))
    # ]
    # res = requests.post(ATEapi_endpoint, files=files)
    # # res.status_code
    # # res.text
    #
    # return res.text, res.status_code
    #
    # example_data = ""
    # with open("C:\\Users\\Kiki\\Desktop\\Untitled-2.json", "r", encoding='utf-8') as f:
    #     example_data = json.loads(f.read())
    #
    # d = 0
    #
    # ret = {'terminoloski_kandidati': [
    #     {
    #         'POSoznake': tk['msd'],
    #         'kandidat': tk['terms'],  # more to bit lemma al terms?
    #         'kanonicnaoblika': tk['canonical'],
    #         'ranking': tk['ranking'],
    #         'podporneutezi': [
    #             6.0274563,  # ????????
    #             6.0274563  # ??????
    #         ],
    #         'pogostostpojavljanja': [101, 71]  # ???????
    #     }
    #     for tk in example_data
    # ]}

    data = {
        "terminoloski_kandidati": [
            {
                "POSoznake": "Ncmsn",
                "kandidat": "vpliv",
                "kanonicnaoblika": "vpliv",
                "nosilnautez": 0.8008282,
                "podporneutezi": [
                    6.0274563,
                    6.0274563
                ],
                "pogostostpojavljanja": [101, 71]
            },
            {
                "POSoznake": "Agpnsg Ncnsg",
                "kandidat": "bivalen okolje",
                "kanonicnaoblika": "bivalno okolje",
                "nosilnautez": 0.60254,
                "podporneutezi": [
                    3.263,
                    2.134
                ],
                "pogostostpojavljanja": [27, 11]
            },
            {
                "POSoznake": "Agpmsny Ncmsn Ncmpg",
                "kandidat": "motorični status otrok",
                "kanonicnaoblika": "motorični status otrok",
                "nosilnautez": 0.3324,
                "podporneutezi": [
                    1.221,
                    3.323
                ],
                "pogostostpojavljanja": [31, 51]
            },
            {
                "POSoznake": "Agpnsn Ncnsn",
                "kandidat": "diplomsko delo",
                "kanonicnaoblika": "diplomsko delo",
                "nosilnautez": 0.2008282,
                "podporneutezi": [
                    0.883,
                    1.02
                ],
                "pogostostpojavljanja": [1241, 111]
            }
        ]
    }
    return data
