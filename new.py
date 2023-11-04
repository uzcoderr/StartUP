import json
import threading
import time

from deep_translator import GoogleTranslator
from googletrans import Translator

# def print_and_update():
#     number = 0
#     while True:
#         print(number)
#         number += 1
#         time.sleep(1)
#
# # Create a thread to run the function
# thread = threading.Thread(target=print_and_update)
#
# # Start the thread
# thread.start()

class TranslationEntry:
    def __init__(self, word, number, translation):
        self.word = word
        self.number = number
        self.translation = translation


def translate_json(json_data):
    translator = Translator()

    translated_entries = []
    wow = 0
    for word, number in json_data['word_count'].items():
        wow += 1
        print(wow)
        # print_and_update()
        translation = GoogleTranslator(source='en', target='uz').translate(word)
        translated_entries.append(TranslationEntry(word, number, translation))

    return translated_entries


# Load the JSON file
with open('output.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Translate the JSON data and create TranslationEntry instances
translated_entries = translate_json(data)

# Save the translated data to a new JSON file
output_data = [{'word': entry.word, 'number': entry.number, 'translate': entry.translation} for entry in
               translated_entries]

with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)
