from dataclasses import dataclass

@dataclass
class Learner:
    ID: int
    age: int
    target_lang: str
    primary_lang: str
    all_langs: list
    
    def __init__(self, id: int, age: int, target_lang: str, primary_lang: str, all_langs: list):
        self.id = id
        self.age = age
        self.target_lang = target_lang
        self.primary_lang = primary_lang
        self.all_langs = all_langs
        
    def __str__(self):
        return "Learner(ID: %s, Age: %s, Target Language: %s, Primary Language: %s, Other Languages: %s)" % (self.id, self.age, self.target_lang, self.primary_lang, self.all_langs)
    
    
    
        
    
    
    
        