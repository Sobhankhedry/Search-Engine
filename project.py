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
        inverted_index[token].add(doc_id +1)

# Step 3: Convert sets to lists for easier readability
for token in inverted_index:
    inverted_index[token] = list(inverted_index[token])

# Print the inverted index
for word, doc_ids in inverted_index.items():
    print(f"Word: '{word}' -> Documents: {doc_ids}")

