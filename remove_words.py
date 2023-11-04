import json
import nltk
from nltk.corpus import wordnet

# Download the WordNet dataset (if not already downloaded)
nltk.download('wordnet')

# Load the JSON object
with open('output.json', 'r') as file:
    data = json.load(file)

# Extract the word count dictionary
word_count_dict = data.get("word_count", {})

# Function to check if a word is an English word
def is_english_word(word):
    return bool(wordnet.synsets(word))

# Filter the word count dictionary to keep only English words
english_word_count = {word: count for word, count in word_count_dict.items() if is_english_word(word)}

# Update the JSON object with the filtered word count dictionary
data["word_count"] = english_word_count

# Write the updated JSON object back to the same file
with open('output.json', 'w') as file:
    json.dump(data, file, indent=2)

print("Filtered English words in 'word_count' have been written to output.json.")
