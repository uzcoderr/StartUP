import re
import json
import threading
from collections import Counter
from tqdm import tqdm

from deep_translator import GoogleTranslator
from googletrans import Translator
from nltk.corpus import wordnet


def is_english_word(word):
    return bool(wordnet.synsets(word))


def count_word_occurrences(input_file, output_file):
    with open(input_file, 'r') as file:
        text = file.read()

    # Define the characters to remove and create a regular expression pattern
    characters_to_remove = r'[!?<>,-:->\d]'

    # Use re.sub to replace characters and numbers with spaces
    text_cleaned = re.sub(characters_to_remove, '', text)

    # Tokenize the cleaned text into words
    words = text_cleaned.split()

    # Use Counter to count word occurrences
    word_count = Counter(words)

    result = {
        "word_count": word_count
    }
    removeWords(result, output_file)


def removeWords(data, output_file):
    word_count_dict = data.get("word_count", {})
    english_word_count = {word: count for word, count in word_count_dict.items() if is_english_word(word)}
    data["word_count"] = english_word_count
    translate(data, output_file)


class TranslationEntry:
    def __init__(self, word, number, translation):
        self.word = word
        self.number = number
        self.translation = translation


def translate_word(word, number, translator, results):
    translation = GoogleTranslator(source='en', target='uz').translate(word)
    entry = TranslationEntry(word, number, translation)
    results.append(entry)


def translate(data, output_file):
    translator = Translator()
    print('Translating...')

    translated_entries = []
    threads = []
    total_words = len(data['word_count'])

    with tqdm(total=total_words) as pbar:
        for word, number in data['word_count'].items():
            thread = threading.Thread(target=translate_word, args=(word, number, translator, translated_entries))
            threads.append(thread)
            thread.start()

            # Update the progress bar with each completed translation
            pbar.update(1)

    for word, number in data['word_count'].items():
        thread = threading.Thread(target=translate_word, args=(word, number, translator, translated_entries))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Wait for all threads to finish

    output_data = [{'word': entry.word, 'number': entry.number, 'translate': entry.translation} for entry in
                   translated_entries]

    with open(f'{output_file}.json', 'w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    input_file = input('Input File path: ')
    output_file = input('Movie name: ')
    count_word_occurrences(input_file, output_file)
