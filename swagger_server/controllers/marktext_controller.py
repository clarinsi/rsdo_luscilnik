import connexion
import six

from swagger_server import util


def get_text(body):  # noqa: E501
    """Označi besedilo s classlo/stanzo z uporabo slovenskih modelov ter vrne conll-u format

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = str.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
