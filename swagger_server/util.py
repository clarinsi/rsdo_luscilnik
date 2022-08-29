import datetime
import os.path

import six
import typing
from swagger_server import type_util
import pandas as pd


def _deserialize(data, klass):
    """Deserializes dict, list, str into an object.

    :param data: dict, list or str.
    :param klass: class literal, or string of class name.

    :return: object.
    """
    if data is None:
        return None

    if klass in six.integer_types or klass in (float, str, bool, bytearray):
        return _deserialize_primitive(data, klass)
    elif klass == object:
        return _deserialize_object(data)
    elif klass == datetime.date:
        return deserialize_date(data)
    elif klass == datetime.datetime:
        return deserialize_datetime(data)
    elif type_util.is_generic(klass):
        if type_util.is_list(klass):
            return _deserialize_list(data, klass.__args__[0])
        if type_util.is_dict(klass):
            return _deserialize_dict(data, klass.__args__[1])
    else:
        return deserialize_model(data, klass)


def _deserialize_primitive(data, klass):
    """Deserializes to primitive type.

    :param data: data to deserialize.
    :param klass: class literal.

    :return: int, long, float, str, bool.
    :rtype: int | long | float | str | bool
    """
    try:
        value = klass(data)
    except UnicodeEncodeError:
        value = six.u(data)
    except TypeError:
        value = data
    return value


def _deserialize_object(value):
    """Return an original value.

    :return: object.
    """
    return value


def deserialize_date(string):
    """Deserializes string to date.

    :param string: str.
    :type string: str
    :return: date.
    :rtype: date
    """
    try:
        from dateutil.parser import parse
        return parse(string).date()
    except ImportError:
        return string


def deserialize_datetime(string):
    """Deserializes string to datetime.

    The string should be in iso8601 datetime format.

    :param string: str.
    :type string: str
    :return: datetime.
    :rtype: datetime
    """
    try:
        from dateutil.parser import parse
        return parse(string)
    except ImportError:
        return string


def deserialize_model(data, klass):
    """Deserializes list or dict to model.

    :param data: dict, list.
    :type data: dict | list
    :param klass: class literal.
    :return: model object.
    """
    instance = klass()

    if not instance.swagger_types:
        return data

    for attr, attr_type in six.iteritems(instance.swagger_types):
        if data is not None \
                and instance.attribute_map[attr] in data \
                and isinstance(data, (list, dict)):
            value = data[instance.attribute_map[attr]]
            setattr(instance, attr, _deserialize(value, attr_type))

    return instance


def _deserialize_list(data, boxed_type):
    """Deserializes a list and its elements.

    :param data: list to deserialize.
    :type data: list
    :param boxed_type: class literal.

    :return: deserialized list.
    :rtype: list
    """
    return [_deserialize(sub_data, boxed_type)
            for sub_data in data]


def _deserialize_dict(data, boxed_type):
    """Deserializes a dict and its elements.

    :param data: dict to deserialize.
    :type data: dict
    :param boxed_type: class literal.

    :return: deserialized dict.
    :rtype: dict
    """
    return {k: _deserialize(v, boxed_type)
            for k, v in six.iteritems(data)}


def is_docker() -> bool:
    # todo: better way of checking if we're on docker or if we're in the develoment enviroment
    return not os.path.exists('.env')


def get_conllu_file_path_by_id(file_id):
    r = f'classla_OS2022/conll/rsdo_doc-{file_id}.plainText.conllu'
    if is_docker():
        return r
    return f'../mnt/ssd/ds_ftp/{r}'


def get_original_file_path_by_id(file_id):
    r = f'classla_OS2022/besedila/rsdo_doc-{file_id}.xml'
    if is_docker():
        return r
    return f'../mnt/ssd/ds_ftp/{r}'


def get_tei_file_path_by_id(file_id):
    r = f'classla_OS2022/tei/rsdo_doc-{file_id}.plainText.tei.xml'
    if is_docker():
        return r
    return f'../mnt/ssd/ds_ftp/{r}'


def get_files_by_keywords(kljucnebesede):
    ret = []
    kljucnebesede = [k.lower() for k in kljucnebesede]
    # Temporary solution until connection with mariadb is fixed
    ngrams_path = "classla_OS2022/ngrams/" if is_docker() else "../mnt/ssd/ds_ftp/classla_OS2022/ngrams/"
    print("Looping trough ngrams")
    for path, dirs, files, in os.walk(ngrams_path):
        for i, _file in enumerate(files):
            if i % 200 == 0: print(f"{i}/{len(files)}")
            file = f'{ngrams_path}{_file}'
            data = pd.read_csv(file, sep='\t')
            amount = len(data[data['ngram_len'] == 1 & data['gram_text'].str.lower().isin(kljucnebesede)])
            # this should be 1
            if amount >= 1:
                ret.append(_file[9:][:-12])
    return ret
