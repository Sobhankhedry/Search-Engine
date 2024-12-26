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


# Debug: Print document mapping
print("Document Mapping:")
for doc_id, filename in sorted(doc_mapping):
    print(f"Document {doc_id}: {filename}")



# Step 2: Build the term frequency table and document frequency table
term_frequencies = {}  # Term frequencies per document {doc_id: {term: count}}
document_frequencies = {}  # Document frequencies {term: number of documents containing term}

for doc_id, tokens in documents:
    term_frequencies[doc_id] = {}
    for token in tokens:
        term_frequencies[doc_id][token] = term_frequencies[doc_id].get(token, 0) + 1

        if token not in document_frequencies:
            document_frequencies[token] = set()
        document_frequencies[token].add(doc_id)

# Convert document frequency sets to counts
for term in document_frequencies:
    document_frequencies[term] = len(document_frequencies[term])

# Step 3: Calculate TF-IDF weights
total_documents = len(documents)
tf_idf = {}  # {doc_id: {term: tf-idf}}

for doc_id, term_freqs in term_frequencies.items():
    tf_idf[doc_id] = {}
    total_terms = sum(term_freqs.values())
    for term, count in term_freqs.items():
        tf = count / total_terms  # Term frequency
        idf = math.log(total_documents / (1 + document_frequencies[term]))  # Inverse document frequency
        tf_idf[doc_id][term] = tf * idf





inverted_index = {}
for doc_id, terms in tf_idf.items():
    for term, weight in terms.items():
        if term not in inverted_index:
            inverted_index[term] = []
        inverted_index[term].append((doc_id, weight))

print("\nInverted Index with TF-IDF:")
for term, postings in inverted_index.items():
    formatted_postings = [(doc_id, f"{weight:.4f}") for doc_id, weight in postings]  # Format to 4 decimal places
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

    # Extract only the document IDs (ignore TF-IDF scores)
    doc_ids1 = set(doc[0] for doc in docs1)  # Extract doc_id from (doc_id, tf-idf)
    doc_ids2 = set(doc[0] for doc in docs2)  # Extract doc_id from (doc_id, tf-idf)

    print(f"Docs for '{term1}': {sorted(doc_ids1)}")  # Debug: Print docs for term1
    print(f"Docs for '{term2}': {sorted(doc_ids2)}")  # Debug: Print docs for term2

    # Perform the boolean operation
    if operator == "AND":
        return sorted(doc_ids1 & doc_ids2)  # Intersection
    elif operator == "OR":
        return sorted(doc_ids1 | doc_ids2)  # Union
    elif operator == "NOT":
        return sorted(doc_ids1 - doc_ids2)  # Difference
    else:
        return "Invalid operator. Use AND, OR, or NOT."


while True:
    query = input("Enter a boolean query (or 'exit' to quit): ")
    if query.lower() == "exit":
        break
    result = process_query(query)
    print(f"Documents matching query '{query}': {result}")