import os
from nltk.tokenize import TreebankWordTokenizer
import nltk
import string

folder_path = "C:\\Users\\sobha\\OneDrive\\Desktop\\Sobhan\\University\\term 5\\Information Retrival\\project\\IR-Project\\Documents"
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

tokenizer = TreebankWordTokenizer()
documents = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {file_path}")  
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()  
            content_no_punctuation = remove_punctuation(content)
            tokens = tokenizer.tokenize(content_no_punctuation)  
            documents.append(tokens)
            #documents.append(content_no_punctuation)



inverted_index = {}

for doc_id, tokens in enumerate(documents):
    for token in tokens:
        if token not in inverted_index:
            inverted_index[token] = set()  # Use a set to avoid duplicate entries
        inverted_index[token].add(doc_id)



def process_query(query):
    terms = query.split()
    if len(terms) != 3:
        return "Invalid query format. Use: term1 AND term2, term1 OR term2, term1 NOT term2."

    term1 = terms[0]
    operator = terms[1].upper()
    term2 = terms[2]
    # Get document sets for terms
    docs_term1 = inverted_index.get(term1, set())
    docs_term2 = inverted_index.get(term2, set())
    
    if operator == "AND":
        result = docs_term1 & docs_term2  # Intersection
    elif operator == "OR":
        result = docs_term1 | docs_term2  # Union
    elif operator == "NOT":
        result = docs_term1 - docs_term2  # Difference
    else:
        return "Invalid operator. Use AND, OR, or NOT."

    return result


while True:
    query = input("Enter a boolean query (or 'exit' to quit): ")
    if query.lower() == "exit":
        break
    result = process_query(query)
    print(f"Documents matching query '{query}': {result}")
