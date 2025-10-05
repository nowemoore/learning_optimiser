from phonemizer import phonemize
import numpy as np
import pandas as pd
import subprocess
from wordfreq import word_frequency
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import nltk

## --- PRELOAD FOR FASTER RUNTIME ---
combined_vocab_df = pd.read_csv('vocab_final.csv', encoding='utf-8', index_col=0)

## --- ACTUAL FUNCTIONS --- ##
def get_semantic_embeddings(word_list, model):
    embeddings = []
    for word in word_list:
        print(word)
        embedding = model.encode(word).tolist()
        embeddings.append(embedding)
        print(embedding[:3])
    
    return embeddings

def get_complexity_embeddings(word_list, user_profile):
    target_lang = user_profile['target_lang']
    origin_lang = user_profile['primary_lang']  
    embeddings = []
    
    for word in word_list:
        ## create a brand new vector thingy
        features = []
        
        ## spelling length
        features.append(len(word))
        
        ## ipa length                   
        ipa_string = get_ipa_repre(word, target_lang)
        features.append(len(ipa_string))
        
        ## number of syllables
        IPA_VOWELS = "aeiouɑɐɒæɔəɘɚɛɜɝɞɨɪɯɵøœɶʉʊʌɤʏ"                                    # ~syllable-defining vowels
        syllable_count = 0                                                              # start counter
        syllable_count = sum(1 for i, char in enumerate(ipa_string) 
            if char in IPA_VOWELS and (i == 0 or ipa_string[i-1] not in IPA_VOWELS))    # counts roughly nuclear vowels
        features.append(syllable_count)
        
        ## freq in native lang                                                                                      # access origin lang from profile
        word_origin_lang_v = combined_vocab_df.loc[combined_vocab_df[target_lang] == word, origin_lang].iloc[0]     # translate target word to origin lang; check supported languages by calling `langs_list = GoogleTranslator().get_supported_languages()`    
        features.append(get_word_frequency(word_origin_lang_v, origin_lang))                                        # find freqency in origin lang
        
        ## freq in target lang
        features.append(get_word_frequency(word, target_lang))
        
        ## similarity to any of the bg langs
        features.append(get_best_levenshtein_score(word, target_lang, user_profile['other_langs']))
        
        ## TO-DO: similarity to other words in lang (that user probably knows)

        features = np.array(features)
        norm = np.linalg.norm(features)
        if norm == 0:
            embeddings.append(features)
        else:
            embeddings.append(features / norm) ## append normalised vector
            
    return embeddings


## --- HELPER FUNCTIONS --- ##
def get_ipa_repre(word, lang):    
    ESPEAK_CODE_MAP = {
        'bashkir': 'ba',
        'belarusian': 'be',
        'mandarin': 'cmn',
        'english': 'en',
        'spanish': 'es',
        'persian': 'fa',
        'french': 'fr',
        'guarani': 'gn',
        'hebrew': 'he',
        'italian': 'it',
        'japanese': 'ja',
        'greenlandic': 'kl',
        'kyrgyz': 'ky',
        'latvian': 'lv',
        'nogai': 'nog',
        'romanian': 'ro',
        'russian': 'ru',
        'turkmen': 'tk',
        'turkish': 'tr',
        'ukrainian': 'uk',
        'uzbek': 'uz',
        'tigrinya': 'ti',
        'faroese': 'fo',
        'karakalpak': 'kaa',
        'xextan': 'xex'
    } # see output langs: https://github.com/espeak-ng/espeak-ng/releases
    
    if lang in ESPEAK_CODE_MAP:
        result = subprocess.run([
                'espeak-ng',     
                '--ipa',                             # output in ipa
                '-v', ESPEAK_CODE_MAP[lang],         # specify lang
                '-q',                                # quiet (no audio)
                word
            ], capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode == 0:
        ipa_string = result.stdout.strip()
        return ipa_string
    else:
        return word # note to self: think of how to handle this
    
def get_word_frequency(word, lang):
    WORDFREQ_CODE_MAP = {
        'arabic': 'ar',
        'bangla': 'bn',
        'bosnian': 'bs',
        'bulgarian': 'bg',
        'catalan': 'ca',
        'chinese': 'zh',
        'croatian': 'hr',
        'czech': 'cs',
        'danish': 'da',
        'dutch': 'nl',
        'english': 'en',
        'finnish': 'fi',
        'french': 'fr',
        'german': 'de',
        'greek': 'el',
        'hebrew': 'he',
        'hindi': 'hi',
        'hungarian': 'hu',
        'icelandic': 'is',
        'indonesian': 'id',
        'italian': 'it',
        'japanese': 'ja',
        'korean': 'ko',
        'latvian': 'lv',
        'lithuanian': 'lt',
        'macedonian': 'mk',
        'malay': 'ms',
        'norwegian': 'nb',
        'persian': 'fa',
        'polish': 'pl',
        'portuguese': 'pt',
        'romanian': 'ro',
        'russian': 'ru',
        'slovak': 'sk',
        'slovenian': 'sl',
        'serbian': 'sr',
        'spanish': 'es',
        'swedish': 'sv',
        'tagalog': 'fil',
        'tamil': 'ta',
        'turkish': 'tr',
        'ukrainian': 'uk',
        'urdu': 'ur',
        'vietnamese': 'vi'
    } # check out documentation for more: https://pypi.org/project/wordfreq/
    
    return word_frequency(word, WORDFREQ_CODE_MAP[lang])

def get_best_levenshtein_score(word, target_lang, all_langs):
    top_similarity_score = -1
    word_ipa = get_ipa_repre(word, target_lang)
    
    for lang in all_langs:
        ## get ipa repre of word in bg lang
        word_bg_lang = combined_vocab_df.loc[combined_vocab_df[target_lang] == word, lang].iloc[0] 
        word_bg_lang_ipa = get_ipa_repre(word_bg_lang, lang)
        curr_score = get_levenshtein_score(word_ipa, word_bg_lang_ipa)

        if curr_score > top_similarity_score:
            top_similarity_score = curr_score
            
    return top_similarity_score

def get_levenshtein_score(word1, word2):
    return 1 - nltk.edit_distance(word1, word2) / max(len(word1), len(word2)) # return normalised levenshtein score

