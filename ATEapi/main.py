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
    if len(predicted_terms) == 0:
        return jsonify({'term_example_occurrence': 'No terms found'})
    else:
        df = pd.DataFrame({'term_example_occurrence':predicted_terms,
                        'raw_prob':prob_terms,
                        'lemma':lemma_terms,
                        'term_example_pos':pos_terms,
                        'term_example_msd':msd_terms})
        df = df.drop_duplicates(subset=['lemma','term_example_pos'], keep='first')
        
        df['ranking'] = pd.Series(dtype='float')
        for i in range(len(df)):
            temp = [float(x) for x in df['raw_prob'].iloc[i].split(' ')]
            df['ranking'].iloc[i] = round(sum(temp)/len(temp),4)

        df = df.sort_values(by=['lemma','ranking'], ascending=True)
        df = df.drop_duplicates(subset=['lemma'], keep='last')
        df['canonical'] = process(df['term_example_occurrence']) 
        corpus = ' '.join([' '.join(x) for x in lemma])
        df['frequency'] = [corpus.count(x) for x in df['lemma']]
        df = df[[ 'lemma', 'canonical', 'frequency','ranking','term_example_occurrence', 'term_example_pos','term_example_msd']]
        df = df[df['term_example_pos'] != 'PUNCT']
        df = df.query("term_example_occurrence.str.len() > 2")
        df = df.drop_duplicates(subset=['term_example_occurrence','lemma'], keep = 'first')
        df = df.sort_values(by=['ranking'], ascending=False)
        # print(df.head(5))
        return df.to_json(orient='records')


if __name__ == '__main__':

    app.run(debug=True)
