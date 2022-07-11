import connexion
import six
import os

from swagger_server.models.terminoloski_kandidat import TerminoloskiKandidat  # noqa: E501
from swagger_server import util
from flask import send_file
from swagger_server.db_utils import Ngrams_Manager


def get_conllu(file_id):  # noqa: E501
    """Vrne CoNNL-U po id-ju datoteke

     # noqa: E501

    :param file_id:
    :type file_id: int

    :rtype: str
    """
    try:
        return send_file(util.get_conllu_path_by_id(file_id), attachment_filename=f'{file_id}.conllu')
    except FileNotFoundError as e:
        return "The conllu with this ID doesn't exist.", 404


def get_conllus(leta, vrste, kljucnebesede, cerifpodrocja):  # noqa: E501
    """Vrne seznam CoNNL-U-jev glede na iskalne pogoje

     # noqa: E501

    :param leta: 
    :type leta: List[int]
    :param vrste: 
    :type vrste: List[str]
    :param kljucnebesede: 
    :type kljucnebesede: List[str]
    :param cerifpodrocja: 
    :type cerifpodrocja: List[int]

    :rtype: List[str]
    """
    return 'do some magic!'


def get_extracted_words(leta, vrste, kljucnebesede, cerifpodrocja):  # noqa: E501
    """Vrne terminloške kandidate glede na 

     # noqa: E501

    :param leta: 
    :type leta: List[int]
    :param vrste: 
    :type vrste: List[str]
    :param kljucnebesede: 
    :type kljucnebesede: List[str]
    :param cerifpodrocja: 
    :type cerifpodrocja: List[int]

    :rtype: List[TerminoloskiKandidat]
    """
    return 'do some magic!'


def get_file(file_id):  # noqa: E501
    """Vrne binarni zapis v originalnem formatu po id-ju datoteke

     # noqa: E501

    :param file_id:
    :type file_id: int

    :rtype: List[bytearray]
    """
    return 'do some magic!'


def get_files(leta, vrste, kljucnebesede, cerifpodrocja):  # noqa: E501
    """Vrne seznam binarnih zapisov v originalnem formatu glede na iskalne pogoje

     # noqa: E501

    :param leta: 
    :type leta: List[int]
    :param vrste: 
    :type vrste: List[str]
    :param kljucnebesede: 
    :type kljucnebesede: List[str]
    :param cerifpodrocja: 
    :type cerifpodrocja: List[int]

    :rtype: List[List[bytearray]]
    """
    return 'do some magic!'


def get_number_texts(leta, vrste, kljucnebesede, cerifpodrocja):  # noqa: E501
    """Vrne število besedil glede na iskalne pogoje

     # noqa: E501

    :param leta: 
    :type leta: List[int]
    :param vrste: 
    :type vrste: List[str]
    :param kljucnebesede: 
    :type kljucnebesede: List[str]
    :param cerifpodrocja: 
    :type cerifpodrocja: List[int]

    :rtype: int
    """
    return 'do some magic!'


def get_texts(leta, vrste, kljucnebesede, cerifpodrocja):  # noqa: E501
    """Vrne seznam besedil glede na iskalne pogoje

     # noqa: E501

    :param leta: 
    :type leta: List[int]
    :param vrste: 
    :type vrste: List[str]
    :param kljucnebesede: 
    :type kljucnebesede: List[str]
    :param cerifpodrocja: 
    :type cerifpodrocja: List[int]

    :rtype: List[str]
    """
    return 'do some magic!'


def oss_besedilo_po_id_get(file_id):  # noqa: E501
    """Vrne besedilo po id-ju datoteke

     # noqa: E501

    :param file_id:
    :type file_id: int

    :rtype: str
    """
    try:
        return send_file(util.get_original_file_by_id(file_id), attachment_filename=f'{file_id}.conllu')
    except FileNotFoundError as e:
        return "The conllu with this ID doesn't exist.", 404
