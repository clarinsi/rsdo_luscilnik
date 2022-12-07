# Dependencies
import torch
import torch.nn.functional as F
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

from utils import *
from canonical_utils import *
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForTokenClassification 

# Your API definition
app = Flask(__name__)

label_list=["n", "B-T", "T"]
tokenizer = AutoTokenizer.from_pretrained('./model/term_extractor/')
model = AutoModelForTokenClassification.from_pretrained('./model/term_extractor/', num_labels=len(label_list)).to(device)

@app.route('/predict',methods=['POST'])
def predict():
    frame = read_conll(request.files['file'])
    sequences = [' '.join(x) for x in frame.word]
    lemma, pos, msd = frame.lemma, frame.pos, frame.msd
    preds = []
    probs = []
    for seq in sequences:
        tokens = tokenizer(seq, padding=True, truncation=True, return_tensors="pt").to(device)
        output = model(**tokens).logits.argmax(-1)
        prob = F.softmax(model(**tokens).logits, dim=2)
        probs.append(prob[0].tolist())
        preds.append([label_list[key] for key in output[0].tolist()])

    texts, final_preds, final_probs = [], [], []
    for seq, pred, prob in list(zip(sequences, preds, probs)):
        t, p, p1 = remap(tokenizer, seq, pred, prob)
        texts.append(t)
        final_preds.append(p)
        final_probs.append(p1)
    predicted_terms, prob_terms, lemma_terms, pos_terms, msd_terms = extract_terms_full(final_preds, final_probs, texts, lemma, pos, msd)
    df = pd.DataFrame({'terms':predicted_terms,
                    'raw_prob':prob_terms,
                    'lemma':lemma_terms,
                    'pos':pos_terms,
                    'msd':msd_terms})
    df = df.drop_duplicates(subset=['lemma','pos'], keep='first')
    # print(df.head(5))
    df['prob'] = pd.Series(dtype='float')
    for i in range(len(df)):
        temp = [float(x) for x in df['raw_prob'].iloc[i].split(' ')]
        df['prob'].iloc[i] = round(sum(temp)/len(temp),4)

    df = df.sort_values(by=['lemma','prob'], ascending=True)
    df = df.drop_duplicates(subset=['lemma'], keep='last')
    df['canonical'] = process(df['terms'])
    df = df[['terms', 'canonical', 'lemma','pos','msd','prob']].rename(columns={'prob':'ranking'})
    # sort by ranking 
    # print(df.head(5))
    df = df[df['pos'] != 'PUNCT']
    df = df.query("terms.str.len() > 2")
    df = df.sort_values('ranking', ascending=False).drop_duplicates(subset=['terms','lemma'], keep = 'first').sort_index()
    print(df.head(5))
    return df.to_json(orient='records')
    # return jsonify(df.to_dict(orient='records'))


if __name__ == '__main__':

    app.run(debug=True)
