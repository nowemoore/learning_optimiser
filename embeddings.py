import subprocess
from wordfreq import word_frequency
from deep_translator import GoogleTranslator
import nltk
# import gensim.downloader as api
from sentence_transformers import SentenceTransformer

## --- ACTUAL FUNCTIONS --- ##
def init_user_profile(age, l1, l2):
    return {'age': age, 'first_lang': l1, 'other_langs': [l1]+l2}

def get_semantic_embedding(word, model):
    ## note to self: figure out fasttext
    vec = model.encode(word)
    return vec

def get_complexity_embedding(word, target_lang, user_profile):
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
    
    ## freq in native lang 
    origin_lang = user_profile['first_lang']                                                        # access origin lang from profile
    word_origin_lang_v = GoogleTranslator(source=target_lang, target=origin_lang).translate(word)   # translate target word to origin lang; check supported languages by calling `langs_list = GoogleTranslator().get_supported_languages()`    
    features.append(get_word_frequency(word_origin_lang_v, origin_lang))                            # find freqency in origin lang
    
    ## freq in target lang
    features.append(get_word_frequency(word, target_lang))
    
    ## similarity to any of the bg langs
    features.append(get_best_levenshtein_score(word, target_lang, user_profile['other_langs']))
    
    # TO-DO: similarity to other words in lang

    return features


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
        word_bg_lang = GoogleTranslator(source=target_lang, target=lang).translate(word)
        word_bg_lang_ipa = get_ipa_repre(word_bg_lang, lang)
        curr_score = get_levenshtein_score(word_ipa, word_bg_lang_ipa)

        if curr_score > top_similarity_score:
            top_similarity_score = curr_score
            
    return top_similarity_score

def get_levenshtein_score(word1, word2):
    return 1 - nltk.edit_distance(word1, word2) / max(len(word1), len(word2)) # return normalised levenshtein score

    
# test_user_profile = init_user_profile(54, "english", ["russian"])
# print(get_complexity_embedding("main", "french", test_user_profile))

