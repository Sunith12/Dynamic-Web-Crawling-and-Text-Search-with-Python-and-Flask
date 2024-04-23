from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import wordnet as wn
from nltk.metrics import edit_distance

app = Flask(__name__)

# Load the inverted index and vectorizer
with open('inverted_index.pkl', 'rb') as f:
    inverted_index = pickle.load(f)
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Define file_paths globally at the top of your script if they are static
file_paths = [
    './documents/books.toscrape.com.html',
    './documents/index.html.html',
    './documents/page-1.html.html',
    './documents/page-2.html.html',
    './documents/page-3.html.html',
    './documents/page-4.html.html'
]


def validate_query(query):
    if not query:
        return False, "Query cannot be empty."
    return True, ""


def correct_spelling(query):
    tokens = query.split()
    corrected_tokens = []
    for token in tokens:
        synsets = wn.synsets(token)
        if synsets:
            corrected_tokens.append(token)
        else:
            # Find closest word by edit distance
            dictionary = vectorizer.get_feature_names_out()
            closest_word, min_dist = None, float('inf')
            for word in dictionary:
                dist = edit_distance(token, word)
                if dist < min_dist:
                    closest_word, min_dist = word, dist
            corrected_tokens.append(closest_word if closest_word else token)
    return ' '.join(corrected_tokens)


def expand_query(query):
    tokens = query.split()
    expanded_query = set(tokens)
    for token in tokens:
        synsets = wn.synsets(token)
        lemmas = {lemma.name() for syn in synsets for lemma in syn.lemmas()}
        expanded_query.update(lemmas)
    return list(expanded_query)


def rank_documents(query, k):
    query_vec = vectorizer.transform([query])
    scores = np.zeros(len(file_paths))
    for idx, word in enumerate(query.split()):
        if word in inverted_index:
            docs = inverted_index[word]
            for doc_id, tfidf_val in docs.items():
                scores[doc_id] += (tfidf_val * query_vec[0, idx])
    top_k_idx = np.argsort(-scores)[:k]
    return top_k_idx.tolist()  # Convert ndarray to list


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def process_query():
    # Check if the incoming request is JSON
    if request.is_json:
        data = request.get_json()
        query = data.get('query')
        k = int(data.get('k', 5))
    else:
        # Handle form data if it's not JSON
        query = request.form.get('query')
        k = int(request.form.get('k', 5))

    # Assuming validate_query, correct_spelling, expand_query, and rank_documents are defined elsewhere
    valid, message = validate_query(query)
    if not valid:
        return jsonify({'error': message}), 400

    query = correct_spelling(query)
    expanded_query = expand_query(query)
    result_indices = rank_documents(' '.join(expanded_query), k)

    # Create a response dictionary
    response = {
        'original_query': query,
        'expanded_query': expanded_query,
        'results': result_indices
    }

    # Check if the request expects a JSON response
    if request.is_json:
        return jsonify(response)
    else:
        # If the request came from a form, you might want to return HTML instead
        return render_template('results.html', response=response)


if __name__ == '__main__':
    app.run(debug=True)
