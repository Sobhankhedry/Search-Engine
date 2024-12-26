import os
from nltk.tokenize import TreebankWordTokenizer
import nltk
import string
import re
import math
tokenizer = TreebankWordTokenizer()


folder_path = "C:\\Users\\sobha\\OneDrive\\Desktop\\Sobhan\\University\\term 5\\Information Retrival\\project\\IR-Project\\Documents"
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))


documents = []  
doc_mapping = []  

for filename in sorted(os.listdir(folder_path)):  
    if filename.endswith(".txt"):
        doc_id = int(re.search(r'\d+', filename).group())
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            content_no_punctuation = remove_punctuation(content)
            tokens = tokenizer.tokenize(content_no_punctuation)
            documents.append((doc_id, tokens))  
            doc_mapping.append((doc_id, filename))  





term_frequencies = {}  
document_frequencies = {}  

for doc_id, tokens in documents:
    term_frequencies[doc_id] = {}
    for token in tokens:
        term_frequencies[doc_id][token] = term_frequencies[doc_id].get(token, 0) + 1

        if token not in document_frequencies:
            document_frequencies[token] = set()
        document_frequencies[token].add(doc_id)


for term in document_frequencies:
    document_frequencies[term] = len(document_frequencies[term])


total_documents = len(documents)
tf_idf = {}  

for doc_id, term_freqs in term_frequencies.items():
    tf_idf[doc_id] = {}
    total_terms = sum(term_freqs.values())
    for term, count in term_freqs.items():
        tf = count / total_terms  
        idf = math.log(total_documents / (1 + document_frequencies[term]))  
        tf_idf[doc_id][term] = tf * idf





inverted_index = {}
for doc_id, terms in tf_idf.items():
    for term, weight in terms.items():
        if term not in inverted_index:
            inverted_index[term] = []
        inverted_index[term].append((doc_id, weight))



print("\nInverted Index with TF-IDF:")
for term, postings in inverted_index.items():
    formatted_postings = [(doc_id, f"{weight:.4f}") for doc_id, weight in postings]  
    print(f"Term: '{term}' -> {formatted_postings}")




def get_matching_docs(term):
    if '*' in term or '?' in term:
        regex = re.compile(f"^{term.replace('*', '.*').replace('?', '.')}$")
        matched_terms = []
        matched_docs = set()
        for word in inverted_index:
            if regex.match(word):
                matched_terms.append(word)  
                matched_docs.update(inverted_index[word]) 
        print(f"Matching terms for '{term}': {matched_terms}") 
        return matched_docs
    else:
        if term in inverted_index:
            print(f"Exact match for '{term}': {[term]}")  
        return inverted_index.get(term, set())

def process_query(query):
    """Process boolean queries with wildcard support"""
    terms = query.split()
    if len(terms) != 3:
        return "Invalid query format. Use: term1 AND term2, term1 OR term2, term1 NOT term2."

    term1, operator, term2 = terms[0], terms[1].upper(), terms[2]

    # Get the matching documents (including TF-IDF scores)
    docs1 = get_matching_docs(term1)
    docs2 = get_matching_docs(term2)

    # Extract only the document IDs and their TF-IDF scores
    doc_ids1_with_scores = {doc_id: tf_idf for doc_id, tf_idf in docs1}  # {doc_id: tf-idf}
    doc_ids2_with_scores = {doc_id: tf_idf for doc_id, tf_idf in docs2}  # {doc_id: tf-idf}

    print(f"Docs for '{term1}': {[(doc_id, f'{score:.4f}') for doc_id, score in doc_ids1_with_scores.items()]}")
    print(f"Docs for '{term2}': {[(doc_id, f'{score:.4f}') for doc_id, score in doc_ids2_with_scores.items()]}")

    # Extract only the document IDs for set operations
    doc_ids1 = set(doc_ids1_with_scores.keys())
    doc_ids2 = set(doc_ids2_with_scores.keys())

    # Perform the boolean operation
    if operator == "AND":
        matching_docs = doc_ids1 & doc_ids2  # Intersection
    elif operator == "OR":
        matching_docs = doc_ids1 | doc_ids2  # Union
    elif operator == "NOT":
        matching_docs = doc_ids1 - doc_ids2  # Difference
    else:
        return "Invalid operator. Use AND, OR, or NOT."

    # Show results with TF-IDF scores
    results_with_scores = []
    for doc_id in matching_docs:
        score1 = doc_ids1_with_scores.get(doc_id, 0)
        score2 = doc_ids2_with_scores.get(doc_id, 0)
        total_score = score1 + score2
        results_with_scores.append((doc_id, total_score))

    # Sort results by TF-IDF scores
    results_with_scores.sort(key=lambda x: x[1], reverse=True)

    return results_with_scores

while True:
    query = input("Enter a boolean query (or 'exit' to quit): ")
    if query.lower() == "exit":
        break
    result = process_query(query)
    print(f"Documents matching query '{query}': {result}")