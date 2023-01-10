import classla
import time
from swagger_server import util
from pathlib import Path
import re

nlp_loaded = False
nlpSlo = classla.Pipeline('sl', processors='tokenize,ner,pos,lemma,depparse')
nlp_loaded = True

sent_extractor = re.compile(r"# sent_id = \d+\.\d+(.*?)\n\n", re.MULTILINE | re.DOTALL)


def raw_text_to_conllu(text):
    try:
        if text == '' or text is None:
            raise Exception("Text can not be empty (when trying to make conllu for it)")
        docall = nlpSlo(text)
        docallconllu = docall.to_conll()

        return docallconllu, 200
    except Exception as e:
        return e, 400


def multipla_conllus_to_one_from_file_ids(list_file_ids):
    sent_cnt = 1
    ret = "# newpar id = 1\n"
    files = [f'{util.get_conllu_file_path_by_id(i)}' for i in list_file_ids]
    for file in files:
        txt = Path(file).read_text('utf-8')
        matches = sent_extractor.finditer(txt)
        for match in matches:
            ret += f'# sent_id = 1.{sent_cnt}{match.group(1)}\n\n'
            sent_cnt += 1

    return ret


def multipla_conllus_to_one_from_conllus_arr(list_conllus):
    sent_cnt = 1
    ret = "# newpar id = 1\n"
    for conllu in list_conllus:
        conllu = conllu.replace('\r\n', '\n')
        matches = sent_extractor.finditer(conllu)
        for match in matches:
            ret += f'# sent_id = 1.{sent_cnt}{match.group(1)}\n\n'
            sent_cnt += 1

    return ret
