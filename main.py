import re
import json

def extract_unique_words(input_file, output_file):
    with open(input_file, 'r') as file:
        text = file.read()

    # Define the characters to remove and create a regular expression pattern
    characters_to_remove = r'[<>!?,-:->123456789]'

    # Use re.sub to replace characters and numbers with spaces
    # text_cleaned = re.sub(characters_to_remove, ' ', text)
    text_cleaned = re.sub(characters_to_remove,'', text)

    # Tokenize the cleaned text into words
    words = text_cleaned.split()

    # Remove duplicate words by converting the list to a set and back to a list
    unique_words = list(set(words))

    result = {
        "unique_words": unique_words
    }

    with open(output_file, 'w') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    input_file = 'words.txt'
    output_file = 'output.json'
    extract_unique_words(input_file, output_file)
