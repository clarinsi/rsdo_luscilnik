from swagger_server import db_utils
from swagger_server import util
from flask import send_file


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
    if not kljucnebesede:
        return "Manjkajo kljucne besede", 400
    files = db_utils.get_files_by_udc(kljucnebesede)
    if not files:
        return 'Nobena datoteka ne ustreza iskalnemu pogoju', 404
    return ' '.join(files), 200


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
    return 'do some magic!5'


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
    if not kljucnebesede:
        return "Manjkajo kljucne besede", 400
    files = db_utils.get_files_by_udc(kljucnebesede)
    if not files:
        return 'Nobena datoteka ne ustreza iskalnemu pogoju', 404
    return ' '.join(files), 200


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
    :type udc: List[int]

    :rtype: int
    """
    if not kljucnebesede:
        return "Manjkajo kljucne besede", 400
    files = db_utils.get_files_by_udc(kljucnebesede)
    return len(files), 200


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
    if not kljucnebesede:
        return "Manjkajo kljucne besede", 400
    files = db_utils.get_files_by_udc(kljucnebesede)
    if not files:
        return 'Nobena datoteka ne ustreza iskalnemu pogoju', 404
    return ' '.join(files), 200


def get_conllu(file_id):  # noqa: E501
    """Vrne CoNNL-U po id-ju datoteke

     # noqa: E501

    :param file_id:
    :type file_id: int

    :rtype: str
    """
    try:
        return send_file(util.get_conllu_file_path_by_id(file_id), download_name=f'{file_id}.conllu')
    except FileNotFoundError as e:
        return "The conllu with this ID doesn't exist.", 404


def get_file(file_id):  # noqa: E501
    """Vrne binarni zapis v originalnem formatu po id-ju datoteke

     # noqa: E501

    :param file_id:
    :type file_id: int

    :rtype: List[bytearray]
    """
    try:
        return send_file(util.get_original_file_path_by_id(file_id), download_name=f'{file_id}.xml')
    except FileNotFoundError as e:
        return "The file with this ID doesn't exist.", 404


def oss_besedilo_po_id_get(file_id):  # noqa: E501
    """Vrne besedilo po id-ju datoteke

     # noqa: E501

    :param file_id:
    :type file_id: int

    :rtype: str
    """
    try:
        f = util.get_original_file_path_by_id(file_id)
        print(f) # for debugging purposes on the server, delete this later
        return send_file(util.get_original_file_path_by_id(file_id), download_name=f'{file_id}.xml')
    except FileNotFoundError as e:
        return "The file with this ID doesn't exist.", 404
