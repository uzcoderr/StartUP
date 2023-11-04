import json
import re

import nltk
from deep_translator import GoogleTranslator
from googletrans import Translator
from collections import defaultdict


class WordTranslation:
    def __init__(self, word, repeat, translate, is_english):
        self.word = word
        self.repeat = repeat
        self.translate = translate
        self.is_english = is_english


def translate_to_uzbek(translator, batch):
    return GoogleTranslator(source='en', target='uz').translate(batch)


def process_text_file(input_file):
    word_count = defaultdict(int)

    with open(input_file, 'r') as file:
        text = file.read()

    # Split the text into words
    words = re.findall(r'\b\w+\b', text.lower())

    translator = Translator()
    batch_size = 50
    translations = []

    for word in words:
        is_english = is_english_word(word)

        if is_english:
            word_count[word] += 1
            translations.append((word, None))

            if len(translations) == batch_size:
                batch_words, _ = zip(*translations)
                translated_batch = translate_to_uzbek(translator, ' '.join(batch_words))

                for i, translation in enumerate(translated_batch.split()):
                    translations[i] = (translations[i][0], translation)

                write_translations_to_json(translations)
                translations = []

    if translations:
        batch_words, _ = zip(*translations)
        translated_batch = translate_to_uzbek(translator, ' '.join(batch_words))

        for i, translation in enumerate(translated_batch.split()):
            translations[i] = (translations[i][0], translation)

        write_translations_to_json(translations)


def write_translations_to_json(translations):
    translated_words = [WordTranslation(word, 1, translation, True) for word, translation in translations]

    with open('word_translations.json', 'a', encoding='utf-8') as json_file:
        json.dump([word.__dict__ for word in translated_words], json_file, ensure_ascii=False, indent=4)

def is_english_word(word):
    english_words = set(nltk.corpus.words.words())
    return word in english_words

if __name__ == "__main__":
    input_file = "words.txt"
    process_text_file(input_file)
