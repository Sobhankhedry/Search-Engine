import os
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk

folder_path = "C:\\Users\\sobha\\OneDrive\\Desktop\\Sobhan\\University\\term 5\\Information Retrival\\project\\IR-Project\\Documents"


documents = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {file_path}")  # Debug: Print file being processed
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()  # Convert text to lowercase
            documents.append(content)

# Check if documents were added
print("Documents list:", documents)

# Print each document
for i, doc in enumerate(documents):
    print(f"Document {i+1}:")
    print(doc)
    print("-" * 50)