from flask import Flask, request, jsonify
from numpy import dot
from numpy.linalg import norm
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import numpy as np
import networkx as nx
import nltk

nltk.download('vader_lexicon') # do we need do to these every time?
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

def cos_sim(a, b): # calculates cosine distance because we want similar sentences to be ignored
    return 1 - dot(a, b)/(norm(a)*norm(b))

def sent_sim(sent_1, sent_2):
    # sent_1 = list(word_tokenize(sent_1))
    # sent_2 = list(word_tokenize(sent_2))
    tokens = set(sent_1)
    tokens.update(sent_2)
    tokens = list(tokens)
    
    tokens_dict = {}
    for i in range(len(tokens)):
        tokens_dict[tokens[i]] = i
    
    token_1 = [0 for i in range(len(tokens))]
    token_2 = [0 for i in range(len(tokens))]
    for i in range(len(sent_1)):
        token_1[tokens_dict[sent_1[i]]] += 1
    for i in range(len(sent_2)):
        token_2[tokens_dict[sent_2[i]]] += 1
    # print(token_1, token_2)
    return cos_sim(token_1, token_2)

def preprocessText(text):
    sent_tokens = sent_tokenize(text)
    stemmer = PorterStemmer()
    for i in range(len(sent_tokens)):
        tokens = word_tokenize(sent_tokens[i])
        tokens = [word.lower() for word in tokens if word.isalpha()]
        filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
        stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
        
        sent_tokens[i] = ' '.join(stemmed_tokens)
        sent_tokens[i] = sent_tokens[i].split()
    return sent_tokens

def initialize_matrix(n):
    mat = []
    for i in range(n):
        mat.append([])
        for j in range(n):
            mat[i].append(0)
    return mat       

def similarity_matrix(textList):
    mat = initialize_matrix(len(textList))
    
    for i in range(len(textList)):
        for j in range(len(textList)):
            if textList[i] is textList[j]:
                mat[i][j] = 0
            else:
                mat[i][j] = sent_sim(textList[i], textList[j])
#                 if mat[i][j] <= 0.6:
#                     print(textList[i], textList[j], i, j)
    return mat

def create_ranking(sim_mat):
    # print(len(mat))
    mat = np.asarray(sim_mat)
    graph = nx.from_numpy_array(mat)
    ranking  = nx.pagerank(graph)
    sorted_ranking = sorted([(value, key)
                        for (key, value) in ranking.items()], reverse=True)
    return [x[1] for x in sorted_ranking]

def generate_summary(text, num_sentences=10):
    preprocessed = preprocessText(text)
    sim_mat = similarity_matrix(preprocessed)
    ranking = create_ranking(sim_mat)
    sentences = sent_tokenize(text)
    summary = ""
    for i in range(min(len(sentences), num_sentences)):
        if len(word_tokenize(sentences[ranking[i]])) >= 10:
            summary += sentences[ranking[i]] + " "
    return summary

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        text = data['text']
        summary = generate_summary(text)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)