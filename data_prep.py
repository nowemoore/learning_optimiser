from pypdf import PdfReader
import numpy as np
import pandas as pd
from deep_translator import GoogleTranslator
from embeddings import * 
import nltk
from sentence_transformers import SentenceTransformer

## read pdf with words
def read_pdf(file_name):
    reader = PdfReader(file_name)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    lines = text.split("\n")
    
    return lines

## extract words as list
def get_vocab_as_list(lines):   
    vocab = []
    
    for line in lines[4:3009] + lines[3012:]: ## (skipping readme lines)
        words_on_line = line.split(" ")
        vocab.append(words_on_line[0])
    
    return vocab

## save list as csv
def save_vocab_as_csv(list):
    np.savetxt("vocab.csv", list, delimiter=",", fmt='%s')
    

## get translations
def get_translations(file_name):
    df = pd.read_csv(file_name, encoding='latin1', index_col=0)
    for language in ["fr", "es", "de", "ru", "pl"]:
       df[language] = ""
    
    idx = 0
    for english_word in df["en"]:
        for language in ["fr", "es", "de", "ru", "pl"]:
            df.loc[idx, language] = GoogleTranslator(source="en", target=language).translate(english_word) 
        print(df.iloc[[idx]])  
        idx += 1 
        if idx % 10 == 0: ## save every 10 to prevent losses to dc
            df.to_csv("vocab_intermed.csv", index=True, encoding='utf-8')

    df.to_csv("vocab_final.csv", index=True, encoding='utf-8')
    
def get_embeddings(file_name):
    df = pd.read_csv(file_name, encoding='utf-8', index_col=0)
    model = SentenceTransformer("distiluse-base-multilingual-cased-v1")    
    
    for language in ["en","fr", "es", "de", "ru", "pl"]:
        df[f"{language}_embedding"] = df.get  