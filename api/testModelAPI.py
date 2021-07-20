from flask import Flask,request,json
from flask_cors import CORS
import re
import pickle


app = Flask(__name__)
CORS(app)

with open('xgb.pkl', 'rb') as handle:
    model = pickle.load(handle)
with open('5000vect.pkl', 'rb') as handle:
    vect = pickle.load(handle)
with open('contraction_mapping.pkl', 'rb') as handle:
    contraction_mapping = pickle.load(handle)
with open('stopwords.pkl', 'rb') as handle:
    stopwords = pickle.load(handle)

def clean(reg_exp, text):
    text = re.sub(reg_exp, " ", text)
    text = re.sub('\s{2,}', ' ', text)
    return text

def remove_urls(text):
    text = clean(r"http\S+", text)
    text = clean(r"www\S+", text)
    text = clean(r"pic.twitter.com\S+", text)
    return text

def prepocess1(text):
    email = re.compile(r'[\w\.-]+@[\w\.-]+')
    text = email.sub(r'',text)
    usernames = re.compile(r'@[\w\.-]+')
    text = usernames.sub(r'',text)
    text = remove_urls(text)
    return text

def remove_non_ascii(s):
    s = s.lower()
    return "".join(i for i in s if ord(i) < 128)

def correct_contraction(x, dic = contraction_mapping):
    for word in dic.keys():
        if word in x:
            x = x.replace(word, dic[word])
    
    return x

def remove_stop_words(text,stopwords = stopwords):
    text = text.split()
    text = [w for w in text if not w in stopwords]
    text = " ".join(text)
    return text

def clean_text(x):
    x = prepocess1(x)
    x = remove_non_ascii(x)
    x = correct_contraction(x)
    x = remove_stop_words(x)
    x = re.sub('[^a-zA-Z0-9]' , ' ' ,x)
    x = [w for w in x.split() if len(w)>1]
    x =' '.join(x)
    return x

labels = {
    0:"Negative",
    1:"Neutral",
    2:"Positive"
}

def result(text:str):
    text = clean_text(text)
    text_dtm = vect.transform([text])
    pred = model.predict(text_dtm)
    return labels[int(pred)]
    

@app.route('/textGM', methods = ['GET'])
def getSentiment():
    res = str(request.args.get('text'))
    res = result(res)
    dict_ = {"sentiment":res}
    return json.dumps(dict_)

@app.route('/textPM',methods = ['POST'])
def predict():
    req_json = request.get_json()
    text = req_json['text']
    res = str(text)
    res = result(res)
    dict_ = {"sentiment":res}
    return json.dumps(dict_)

if __name__ == '__main__':
    app.run(debug = True)