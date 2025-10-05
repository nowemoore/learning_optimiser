from dataclasses import dataclass

@dataclass
class Learner:
    ID: int
    age: int
    target_lang: str
    primary_lang: str
    all_langs: list
    seed: int
    user_data: list = None
    knowledge_binary: list = None
    
    def __init__(self, id: int, age: int, seed: int, target_lang: str, primary_lang: str, all_langs: list):
        self.id = id
        self.age = age
        self.target_lang = target_lang
        self.primary_lang = primary_lang
        self.all_langs = all_langs
        self.seed = seed
        
    def __str__(self):
        return "Learner(ID: %s, Age: %s, Target Language: %s, Primary Language: %s, Other Languages: %s)" % (self.id, self.age, self.target_lang, self.primary_lang, self.all_langs)
    
    def collect_data(self, test_words: list):
        known_words = []
        unknown_words = []
        
        for word in test_words:
            response = input(f"Do you know the word '{word}'? (y/n): ").strip().lower()
            if response == 'y':
                known_words.append(word)
            elif response == 'n':
                unknown_words.append(word)
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")
                
        self.set_user_data(known_words, unknown_words)
    
    def set_user_data(self, known_words: list, unknown_words: list):
        knowledge_binary = [(word, 1) for word in known_words] + [(word, 0) for word in unknown_words]
        self.knowledge_binary = knowledge_binary
            
            
        
    
        
    
    
    
        