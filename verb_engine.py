import json
import random
import unicodedata
from config import PERSONS, TENSES, PERSONS_RUSSIAN, TENSES_RUSSIAN, TENSE_GROUPS

class VerbEngine:
    def __init__(self, verbs_file='verbs_data.json', translations_file='verb_translations.json'):
        """Initialize the verb engine with verb data and translations."""
        with open(verbs_file, 'r', encoding='utf-8') as f:
            self.verbs_data = json.load(f)
        with open(translations_file, 'r', encoding='utf-8') as f:
            self.verb_translations = json.load(f)
        self.verb_list = list(self.verbs_data.keys())
    
    def get_random_challenge(self):
        """Generate a random verb conjugation challenge."""
        # Select random verb
        verb = random.choice(self.verb_list)
        
        # Select random tense
        tense = random.choice(list(TENSES.keys()))
        
        # Select random person (0-5 for yo, tú, él/ella, nosotros, vosotros, ellos/ellas)
        person_index = random.randint(0, 5)
        person = PERSONS[person_index]
        
        # Get the correct answer
        correct_answer = self.verbs_data[verb][tense][person_index]
        
        return {
            'verb': verb,
            'tense': tense,
            'tense_display': TENSES[tense],
            'person': person,
            'person_index': person_index,
            'correct_answer': correct_answer
        }
    
    def normalize_text(self, text):
        """Normalize text by removing accents and converting to lowercase."""
        # Remove accents
        text = unicodedata.normalize('NFD', text)
        text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
        # Convert to lowercase and strip whitespace
        return text.lower().strip()
    
    def check_answer(self, user_answer, correct_answer):
        """Check if the user's answer is correct."""
        # Normalize both answers for comparison
        normalized_user = self.normalize_text(user_answer)
        normalized_correct = self.normalize_text(correct_answer)
        
        # Check exact match first
        if user_answer.strip().lower() == correct_answer.lower():
            return True
        
        # Check normalized match (without accents)
        if normalized_user == normalized_correct:
            return True
        
        return False
    
    def get_verb_info(self, verb):
        """Get all conjugations for a specific verb."""
        if verb in self.verbs_data:
            return self.verbs_data[verb]
        return None
    
    def get_total_verbs(self):
        """Get the total number of verbs in the database."""
        return len(self.verb_list)
    
    def get_random_verb(self):
        """Get a random verb from the database."""
        return random.choice(self.verb_list)
    
    def get_random_challenge_by_group(self, tense_group):
        """Generate a random verb conjugation challenge for a specific tense group."""
        # Get tenses for the group
        if tense_group not in TENSE_GROUPS:
            return self.get_random_challenge()
        
        tenses = TENSE_GROUPS[tense_group]['tenses']
        
        # Select random verb
        verb = random.choice(self.verb_list)
        
        # Select random tense from the group
        tense = random.choice(tenses)
        
        # Select random person (0-5 for yo, tú, él/ella, nosotros, vosotros, ellos/ellas)
        person_index = random.randint(0, 5)
        person = PERSONS[person_index]
        
        # Get the correct answer
        correct_answer = self.verbs_data[verb][tense][person_index]
        
        return {
            'verb': verb,
            'tense': tense,
            'tense_display': TENSES[tense],
            'tense_display_ru': TENSES_RUSSIAN[tense],
            'person': person,
            'person_ru': PERSONS_RUSSIAN[person_index],
            'person_index': person_index,
            'correct_answer': correct_answer,
            'verb_translation': self.verb_translations.get(verb, verb),
            'tense_group': tense_group
        }
    
    def get_verb_translation(self, verb):
        """Get Russian translation for a verb."""
        return self.verb_translations.get(verb, verb)
    
    def get_tense_groups(self):
        """Get all available tense groups."""
        return TENSE_GROUPS
    
    def get_random_challenge_by_groups(self, tense_group_keys):
        """Generate a random verb conjugation challenge for multiple tense groups."""
        # Collect all tenses from selected groups
        all_tenses = []
        for group_key in tense_group_keys:
            if group_key in TENSE_GROUPS:
                all_tenses.extend(TENSE_GROUPS[group_key]['tenses'])
        
        # Remove duplicates
        all_tenses = list(set(all_tenses))
        
        if not all_tenses:
            # Fallback to all tenses if no valid groups
            all_tenses = list(TENSES.keys())
        
        # Select random verb
        verb = random.choice(self.verb_list)
        
        # Select random tense from collected tenses
        tense = random.choice(all_tenses)
        
        # Select random person (0-5 for yo, tú, él/ella, nosotros, vosotros, ellos/ellas)
        person_index = random.randint(0, 5)
        person = PERSONS[person_index]
        
        # Get the correct answer
        correct_answer = self.verbs_data[verb][tense][person_index]
        
        return {
            'verb': verb,
            'tense': tense,
            'tense_display': TENSES[tense],
            'person': person,
            'person_index': person_index,
            'correct_answer': correct_answer,
            'verb_translation': self.verb_translations.get(verb, verb),
            'selected_groups': tense_group_keys
        }
