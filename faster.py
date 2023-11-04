from datetime import datetime
import json
import re
import threading

from deep_translator import GoogleTranslator
from googletrans import Translator
import nltk
from collections import defaultdict

# Download the necessary data for nltk if not already downloaded
nltk.download('words')

class WordTranslation:
    def __init__(self, word, repeat, translate, is_english):
        self.word = word
        self.repeat = repeat
        self.translate = translate
        self.is_english = is_english

def translate_to_uzbek(texts):
    translator = Translator()
    translations = []
    max_chars = 6000
    print(datetime.now().second)
    for text in texts:
        # Split text into chunks that are within the character limit
        chunks = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
        chunk_translations = [GoogleTranslator(source='en', target='uz').translate(chunk) for chunk in chunks]
        translations.append(''.join(chunk_translations))

    return translations

def is_english_word(word):
    english_words = set(nltk.corpus.words.words())
    return word in english_words

def process_text_file(input_file):
    word_count = defaultdict(int)

    with open(input_file, 'r') as file:
        for line in file:
            # Remove specified characters and convert to lowercase
            line = re.sub(r'[,"-><?!]', '', line.lower())
            words = line.split()

            for word in words:
                # Skip empty words and words with digits
                if not word or re.search(r'\d', word):
                    continue

                is_english = is_english_word(word)

                if is_english:
                    word_count[word] += 1

    # Extract English words and their counts
    english_words = [word for word, count in word_count.items()]
    word_counts = [count for count in word_count.values()]

    # Batch translation for efficiency
    batch_size = 50  # Adjust the batch size based on your needs
    batches = [english_words[i:i + batch_size] for i in range(0, len(english_words), batch_size)]
    translations = []

    for batch in batches:
        translated_texts = translate_to_uzbek(batch)
        translations.extend(translated_texts)

    # Create WordTranslation objects
    translated_words = []
    for word, count, translation in zip(english_words, word_counts, translations):
        translated_words.append(WordTranslation(word, count, translation, True))

    # Write the translations to a JSON file
    with open('word_translations.json', 'w', encoding='utf-8') as json_file:
        json.dump([word.__dict__ for word in translated_words], json_file, ensure_ascii=False, indent=4)
        print(datetime.now().min)
        print(datetime.now().second)

if __name__ == "__main__":
    print(datetime.now().min)
    print(datetime.now().second)
    input_file = "words.txt"  # Replace with the path to your .txt file
    process_text_file(input_file)
