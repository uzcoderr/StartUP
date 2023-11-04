import json
from googletrans import Translator
from deep_translator import GoogleTranslator


def translate_json(json_data):
    translator = Translator()

    translated_json = {}

    for key, value in json_data.items():
        translated_key = GoogleTranslator(source='en', target='uz').translate(key)
        # translated_key = translator.translate(key, src='en', dest='uz').text
        if isinstance(value, dict):
            translated_value = translate_json(value)  # Recursive call for nested dictionaries
        elif isinstance(value, str):
            translated_value = translator.translate(value, src='en', dest='uz').text
        else:
            translated_value = value  # Leave other data types as they are

        translated_json[translated_key] = translated_value

    return translated_json


# Load the JSON file
with open('output.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Translate the JSON data
translated_data = translate_json(data)

# Save the translated JSON to a new file
with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(translated_data, json_file, ensure_ascii=False, indent=4)
