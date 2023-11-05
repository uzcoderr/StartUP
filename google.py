import re
import json
import threading
from collections import Counter
from nltk.corpus import wordnet
from tqdm import tqdm

import translator
from trasnlate_and_add import translate_word


def is_english_word(word):
    return bool(wordnet.synsets(word))


def count_word_occurrences(input_file, output_file):
    print('count_word_occurrences')
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
    removeWords(result)


def removeWords(data):
    print('removeWords')
    word_count_dict = data.get("word_count", {})
    english_word_count = {word: count for word, count in word_count_dict.items() if is_english_word(word)}
    data["word_count"] = english_word_count
    wordsTranslator(data)


def wordsTranslator(data):
    print('Translating...')
    word_count_dict = data.get("word_count", {})
    progress_bar = tqdm(word_count_dict.items(), desc="Processing", unit=" word")

    english_word_count = {}

    for word, count in progress_bar:
        if is_english_word(word):
            english_word_count[word] = count
    translated_entries = []
    threads = []

    for word, number in data['word_count'].items():
        thread = threading.Thread(target=translate_word, args=(word, number, translator, translated_entries))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Wait for all threads to finish

    output_data = [{'word': entry.word, 'number': entry.number, 'translate': entry.translation} for entry in translated_entries]

    with open('output.json', 'w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    input_file = 'words.txt'
    output_file = 'output.json'
    print('started')
    count_word_occurrences(input_file, output_file)
