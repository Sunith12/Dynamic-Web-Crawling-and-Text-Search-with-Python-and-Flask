# build_index.py
import os
import pickle
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Step 1: Load and parse HTML documents


def load_documents(file_paths):
    texts = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            texts.append(soup.get_text())
    return texts

# Step 2: Compute TF-IDF representation


def compute_tfidf(texts):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix

# Step 3: Build the inverted index
def build_inverted_index(tfidf_matrix, vectorizer):
    # Use get_feature_names instead of get_feature_names_out
    feature_names = vectorizer.get_feature_names()
    inverted_index = {}
    for idx, word in enumerate(feature_names):
        # Extract the row indices where values are non-zero
        doc_ids = tfidf_matrix[:, idx].nonzero()[0]
        values = tfidf_matrix[:, idx].data
        inverted_index[word] = {
            doc_id: value for doc_id, value in zip(doc_ids, values)}
    return inverted_index


# Files to process
file_paths = [
    './documents/books.toscrape.com.html',
    './documents/index.html.html',
    './documents/page-1.html.html',
    './documents/page-2.html.html',
    './documents/page-3.html.html',
    './documents/page-4.html.html'
]  # Update with actual paths

# Main operations
texts = load_documents(file_paths)
vectorizer, tfidf_matrix = compute_tfidf(texts)
inverted_index = build_inverted_index(tfidf_matrix, vectorizer)

# Step 4: Save the inverted index and the vectorizer to pickle files
with open('inverted_index.pkl', 'wb') as f:
    pickle.dump(inverted_index, f)
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Inverted index and vectorizer have been built and saved.")
