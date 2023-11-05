import json
from deep_translator import GoogleTranslator
import threading

from googletrans import Translator


class TranslationEntry:
    def __init__(self, word, number, translation):
        self.word = word
        self.number = number
        self.translation = translation


def translate_word(word, number, translator, results):
    translation = GoogleTranslator(source='en', target='uz').translate(word)
    entry = TranslationEntry(word, number, translation)
    results.append(entry)


def main():
    translator = Translator()
    print('Translating...')

    with open('output.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

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


if __name__ == "__main__":
    main()
