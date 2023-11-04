import json
import re

from deep_translator import GoogleTranslator
from googletrans import Translator
import nltk

# Download the necessary data for nltk if not already downloaded
nltk.download('words')


class WordTranslation:
    def __init__(self, word, repeat, translate, is_english):
        self.word = word
        self.repeat = repeat
        self.translate = translate
        self.is_english = is_english


def translate_to_uzbek(text):
    translator = Translator()
    translated = GoogleTranslator(source='en', target='uz').translate(text)
    return translated


def is_english_word(word):
    english_words = set(nltk.corpus.words.words())
    return word in english_words


def process_text_file(input_file):
    word_count = {}

    with open(input_file, 'r') as file:
        for line in file:
            # Remove specified characters and convert to lowercase
            line = re.sub(r'[,"-><?!]', '', line.lower())
            words = line.split()

            for word in words:
                # Skip empty words
                if not word:
                    continue

                if re.search(r'\d', word):  # Exclude words with digits
                    continue

                is_english = is_english_word(word)

                if word in word_count:
                    word_count[word]["repeat"] += 1
                else:
                    word_count[word] = {
                        "repeat": 1,
                        "translate": translate_to_uzbek(word),
                        "is_english": is_english
                    }

    translations = []
    for word, info in word_count.items():
        word_translation = WordTranslation(word, info["repeat"], info["translate"], info["is_english"])
        translations.append(word_translation.__dict__)

    # Write the translations to a JSON file
    with open('word_translations.json', 'w', encoding='utf-8') as json_file:
        json.dump(translations, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_file = "hello.txt"  # Replace with the path to your .txt file
    process_text_file(input_file)
