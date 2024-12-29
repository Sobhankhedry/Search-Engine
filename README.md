# Boolean Search Engine with TF-IDF and Wildcard Support

This project implements a Boolean search engine with TF-IDF weighting for ranking documents. It allows users to query a collection of documents using boolean operators (`AND`, `OR`, `NOT`) and wildcard characters (`*`, `?`). The engine computes term frequencies, document frequencies, and TF-IDF scores, while also supporting efficient retrieval through an inverted index.

## Features
- **TF-IDF Weighting**: Assigns scores to terms based on their importance in individual documents and across the collection.
- **Inverted Index**: Enables efficient document retrieval for terms and their associated TF-IDF scores.
- **Boolean Query Support**: Handles queries with `AND`, `OR`, and `NOT` operators.
- **Wildcard Search**: Supports `*` (matches zero or more characters) and `?` (matches exactly one character) for term pattern matching.
- **Document Ranking**: Results are ranked by cumulative TF-IDF scores for better relevance.

## How It Works
1. **Document Preprocessing**:
   - Reads text files from a specified folder.
   - Removes punctuation and converts content to lowercase.
   - Tokenizes text into individual terms.

2. **Index Construction**:
   - Calculates term frequencies (TF) for each document.
   - Computes document frequencies (DF) for each term.
   - Builds an inverted index containing terms, document IDs, and their corresponding TF-IDF scores.

3. **Query Processing**:

   - Supports exact term matching and wildcard queries.
   - Processes Boolean queries using set operations (`AND`, `OR`, `NOT`).
   - Ranks matching documents based on cumulative TF-IDF scores.


## Example Output

When you run a query, the script outputs:

- **Matched Documents**: Lists the document IDs and their cumulative TF-IDF scores.
- **Wildcard Matches**: Shows terms that match the wildcard pattern.

### Sample Output
```
Enter a boolean query (or 'exit' to quit): term1 AND term2
Matching terms for 'term1': ['term1']
Matching terms for 'term2': ['term2']
Docs for 'term1': [(1, '0.1234'), (2, '0.5678')]
Docs for 'term2': [(2, '0.3456')]
Documents matching query 'term1 AND term2': [(2, 0.9134)]
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/boolean-search-engine.git
   cd boolean-search-engine
