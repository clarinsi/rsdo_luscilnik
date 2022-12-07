import os
import glob
import json
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def read_conll(f, lowercase=True, max_example=None):
    examples = []
    # with open(in_file) as f:
    word, lemma, pos, msd, label = [], [], [], [], []
    for line in f.readlines():
        sp = line.decode('utf-8').strip().split('\t')
        # print(sp)
        if len(sp) == 10:
            if '-' not in sp[0]:
                word.append(sp[1].lower() if lowercase else sp[1])
                lemma.append(sp[2].lower() if lowercase else sp[2])
                pos.append(sp[3])
                msd.append(sp[4])
                label.append('n')
        elif len(word) > 0:
            examples.append({'word': word, 'lemma': lemma, 'pos': pos, 'msd':msd,   'labels': label})
            word, lemma, pos, msd, label = [], [], [], [], []
            if (max_example is not None) and (len(examples) == max_example):
                break
    if len(word) > 0:
        examples.append({'word': word, 'lemma': lemma, 'pos': pos,  'msd':msd, 'labels': label})
    return pd.DataFrame(examples)


def extract_terms_full(token_predictions,token_probabilities, val_texts, lemma_texts, pos_texts, msd_texts):
    extracted_terms = list()
    extracted_probs = list()
    lemma_terms = list()
    pos_terms = list()
    msd_terms = list()
    # go over all predictions
    for i in range(len(token_predictions)):
        pred = token_predictions[i]
        prob = token_probabilities[i]
        txt  = val_texts[i]
        lemma  = lemma_texts[i]
        pos  = pos_texts[i]
        msd  = msd_texts[i]
        for j in range(len(pred)):
            if pred[j] == "B-T":
                term = txt[j]
                prob_term = str(round(prob[j][1],4))
                lemma_term = lemma[j]
                pos_term = pos[j]
                msd_term = msd[j]
                for k in range(j+1,len(pred)):
                    if pred[k]=="T": 
                        term+=" "+txt[k]
                        prob_term+=" "+str(round(prob[k][2],4))
                        lemma_term+=" "+ lemma[k]
                        pos_term+=" "+ pos[k]
                        msd_term+=" "+ msd[k]
                    else: break
                extracted_terms.append(term)
                extracted_probs.append(prob_term)
                lemma_terms.append(lemma_term)
                pos_terms.append(pos_term)
                msd_terms.append(msd_term)
    return extracted_terms, extracted_probs, lemma_terms, pos_terms, msd_terms

def remap(tokenizer, texts, preds, probs):
    text = texts.split(' ')
    len_token = []
    res_pred = []
    final_pred = []
    res_prob = []
    final_prob = []
    for i in range(len(text)):
        temp = len(tokenizer(text[i], add_special_tokens=False)['input_ids'])
        len_token.append(temp)
    for val in len_token:
        res_pred.append(val)
        res_pred.extend([0]*(val-1))    
        res_prob.append(val)
        res_prob.extend([0]*(val-1))  
    for p1, p2 in zip(res_pred, preds[1:len(preds)-1]):
        if p1 != 0:
            final_pred.append(p2)
    for p1, p2 in zip(res_prob, probs[1:len(probs)-1]):
        if p1 != 0:
            final_prob.append(p2)
    return text, final_pred, final_prob
