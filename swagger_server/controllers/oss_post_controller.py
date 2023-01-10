import connexion
import six

from swagger_server.controllers.oss_controller import get_conllus, get_extracted_words, get_extracted_words_async, \
    get_files, get_number_texts, get_texts
from swagger_server.models.terminoloski_kandidat import TerminoloskiKandidat  # noqa: E501
from swagger_server import util


def get_conllus_post(leta=None, vrste=None, kljucne_besede=None, udk=None):  # noqa: E501
    """Vrne seznam CoNNL-U-jev glede na iskalne pogoje

     # noqa: E501

    :param leta: 
    :type leta: List[int]
    :param vrste: 
    :type vrste: List[int]
    :param kljucne_besede: 
    :type kljucne_besede: List[str]
    :param udk: 
    :type udk: List[str]

    :rtype: List[str]
    """
    return get_conllus(leta, vrste, kljucne_besede, udk)


def get_extracted_words_async_post(leta=None, vrste=None, kljucne_besede=None, prepovedane_besede=None,
                                   udk=None,definicije=False):  # noqa: E501
    """Vrne terminloške kandidate glede na ... (async)

     # noqa: E501

    :param leta: 
    :type leta: List[int]
    :param vrste: 
    :type vrste: List[int]
    :param kljucne_besede: 
    :type kljucne_besede: List[str]
    :param prepovedane_besede: 
    :type prepovedane_besede: List[str]
    :param udk: 
    :type udk: List[str]

    :rtype: str
    """
    return get_extracted_words_async(leta, vrste, kljucne_besede, prepovedane_besede, udk,definicije)


def get_extracted_words_post(leta=None, vrste=None, kljucne_besede=None, prepovedane_besede=None,
                             udk=None,definicije=False):  # noqa: E501
    """Vrne terminloške kandidate glede na ... (sync)

     # noqa: E501

    :param leta: 
    :type leta: List[int]
    :param vrste: 
    :type vrste: List[int]
    :param kljucne_besede: 
    :type kljucne_besede: List[str]
    :param prepovedane_besede: 
    :type prepovedane_besede: List[str]
    :param udk: 
    :type udk: List[str]

    :rtype: List[TerminoloskiKandidat]
    """
    return get_extracted_words(leta, vrste, kljucne_besede, prepovedane_besede, udk,definicije)


def get_files_post(leta=None, vrste=None, kljucne_besede=None, udk=None):  # noqa: E501
    """Vrne seznam binarnih zapisov v originalnem formatu glede na iskalne pogoje

     # noqa: E501

    :param leta: 
    :type leta: List[int]
    :param vrste: 
    :type vrste: List[int]
    :param kljucne_besede: 
    :type kljucne_besede: List[str]
    :param udk: 
    :type udk: List[str]

    :rtype: List[List[bytearray]]
    """
    return get_files(leta, vrste, kljucne_besede, udk)


def get_number_texts_post(leta=None, vrste=None, kljucne_besede=None, udk=None):  # noqa: E501
    """Vrne število besedil glede na iskalne pogoje

     # noqa: E501

    :param leta: 
    :type leta: List[int]
    :param vrste: 
    :type vrste: List[int]
    :param kljucne_besede: 
    :type kljucne_besede: List[str]
    :param udk: 
    :type udk: List[str]

    :rtype: int
    """
    return get_number_texts(leta, vrste, kljucne_besede, udk)


def get_texts_post(leta=None, vrste=None, kljucne_besede=None, udk=None):  # noqa: E501
    """Vrne seznam besedil glede na iskalne pogoje

     # noqa: E501

    :param leta: 
    :type leta: List[int]
    :param vrste: 
    :type vrste: List[int]
    :param kljucne_besede: 
    :type kljucne_besede: List[str]
    :param udk: 
    :type udk: List[str]

    :rtype: List[str]
    """
    return get_texts(leta, vrste, kljucne_besede, udk)
