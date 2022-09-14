import connexion

from swagger_server.models.izlusci_body import IzlusciBody  # noqa: E501


def get_candidates(body):  # noqa: E501
    """Izlusci terminološke kandidate iz seznama besedil v conllu obliki

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: List[TerminoloskiKandidat]
    """
    if connexion.request.is_json:
        body = IzlusciBody.from_dict(connexion.request.get_json())  # noqa: E501

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
