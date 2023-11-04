import re
import json
from collections import Counter


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

    with open(output_file, 'w') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    input_file = 'words.txt'
    output_file = 'output.json'
    count_word_occurrences(input_file, output_file)
