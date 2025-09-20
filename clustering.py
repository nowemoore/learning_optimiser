import pandas as pd
import nltk
from pypdf import PdfReader
from embeddings import * 

## --- CLUSTERING ---

## find top 5,000 nouns and verbs by frequency
reader = PdfReader("all_top_words.pdf")
text = ""

for page in reader.pages:
    text += page.extract_text()

lines = text.split("\n")

vocab = []

for line in lines[4:3009] + lines[3012:]: ## (skipping readme lines)
    words_on_line = line.split(" ")
    vocab.append(words_on_line[0])

## embed top 5,000 words in target language using embeddings.py
model = SentenceTransformer("distiluse-base-multilingual-cased-v1") ## load semantic embed model

for word in vocab:
    print(word)
    print(get_semantic_embedding(word, model)[:3])
    

## compute intertia

## cluster based on intertia computed

## propose a representative for each cluster