import os
from nltk.tokenize import TreebankWordTokenizer
import nltk
import string
import re
tokenizer = TreebankWordTokenizer()
folder_path = "C:\\Users\\sobha\\OneDrive\\Desktop\\Sobhan\\University\\term 5\\Information Retrival\\project\\IR-Project\\Documents"


def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

# Step 1: Parse all documents and store tokens
documents = []  # To store tokenized content for each document
doc_mapping = []  # To map document IDs to filenames for debugging

for filename in sorted(os.listdir(folder_path)):  # Sort filenames for consistent order
    if filename.endswith(".txt"):
        # Extract document ID from filename (e.g., Doc1.txt -> 1)
        doc_id = int(re.search(r'\d+', filename).group())
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            content_no_punctuation = remove_punctuation(content)
            tokens = tokenizer.tokenize(content_no_punctuation)
            documents.append((doc_id, tokens))  # Store (doc_id, tokens)
            doc_mapping.append((doc_id, filename))  # Map doc_id to filename

# Debug: Print document mapping
print("Document Mapping:")
for doc_id, filename in sorted(doc_mapping):
    print(f"Document {doc_id}: {filename}")

# Step 2: Build the inverted index
inverted_index = {}
for doc_id, tokens in documents:
    for token in tokens:
        if token not in inverted_index:
            inverted_index[token] = set()
        inverted_index[token].add(doc_id)  # Correctly map token to doc_id

# Debug: Print the inverted index
print("\nInverted Index:")
for term, doc_ids in sorted(inverted_index.items()):
    print(f"Term: '{term}' -> Documents: {sorted(doc_ids)}")


# Debug: Print the inverted index
print("\nInverted Index:")
for term, doc_ids in inverted_index.items():
    print(f"Term: '{term}' -> Documents: {doc_ids}")


def get_matching_docs(term):
    """Handles both exact matches and wildcard queries (* and ?)"""
    if '*' in term or '?' in term:
        # Replace wildcards with regex equivalents
        regex = re.compile(f"^{term.replace('*', '.*').replace('?', '.')}$")
        matched_terms = []
        matched_docs = set()
        for word in inverted_index:
            if regex.match(word):
                matched_terms.append(word)  # Collect matching terms
                matched_docs.update(inverted_index[word])  # Collect document IDs
        print(f"Matching terms for '{term}': {matched_terms}")  # Debug: print matching terms
        return matched_docs
    else:
        # Exact term
        if term in inverted_index:
            print(f"Exact match for '{term}': {[term]}")  # Debug: print exact match
        return inverted_index.get(term, set())


# Function to process queries
def process_query(query):
    """Process boolean queries with wildcard support"""
    terms = query.split()
    if len(terms) != 3:
        return "Invalid query format. Use: term1 AND term2, term1 OR term2, term1 NOT term2."

    term1, operator, term2 = terms[0], terms[1].upper(), terms[2]
    docs1 = get_matching_docs(term1)
    docs2 = get_matching_docs(term2)

    
    # Debug: Check matched docs for both terms
    print(f"Docs for '{term1}': {docs1}")
    print(f"Docs for '{term2}': {docs2}")

    # Perform boolean operations
    if operator == "AND":
        return docs1 & docs2  # Intersection
    elif operator == "OR":
        return docs1 | docs2  # Union
    elif operator == "NOT":
        return docs1 - docs2  # Difference
    else:
        return "Invalid operator. Use AND, OR, or NOT."

# Main loop
while True:
    query = input("Enter a boolean query (or 'exit' to quit): ")
    if query.lower() == "exit":
        break
    result = process_query(query)
    print(f"Documents matching query '{query}': {result}")