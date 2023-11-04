import json
import nltk
from nltk.corpus import wordnet
from deep_translator import GoogleTranslator
# pip install google_trans_new
# Download the WordNet dataset (if not already downloaded)

# Load the JSON object
with open('output.json', 'r') as file:
    data = json.load(file)

# Extract the word count dictionary
word_count_dict = data.get("word_count", {})


# Function to check if a word is an English word
def is_english_word(word):
    return bool(wordnet.synsets(word))


# Function to translate English word to Uzbek
# Function to translate English word to Uzbek with error handling
def translate_to_uzbek(word):
    x = word
    try:
        x = GoogleTranslator(source='en', target='uz').translate(x)
        print(x)
        return x  # Return the original word if translation is not available
    except Exception as e:
        print(f"Translation error: {e}")
        return x  # Return the original word on error


# Translate and update the word count dictionary
uzbek_word_count = {word: count for word, count in word_count_dict.items() if is_english_word(word)}
uzbek_word_count = {word: count for word, count in uzbek_word_count.items() if translate_to_uzbek(word) != word}

# Update the JSON object with the translated word count dictionary
data["word_count"] = uzbek_word_count

# Write the updated JSON object back to the same file
with open('output.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print("Filtered English words in 'word_count' have been translated to Uzbek and written to output.json.")
