import connexion
import six

from swagger_server.models.izlusci_body import IzlusciBody  # noqa: E501
from swagger_server.models.terminoloski_kandidat import TerminoloskiKandidat  # noqa: E501
from swagger_server import util


def get_candidates(body):  # noqa: E501
    """Izlusci terminološke kandidate iz seznama besedil v conllu obliki

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: List[TerminoloskiKandidat]
    """
    if connexion.request.is_json:
        body = IzlusciBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
