import pandas as pd
import re
from collections import Counter

# ----------------- NormalizedInput Class -----------------
class NormalizedInput:  
    """
    A class to normalize and process text data from a CSV file.
    It reads a CSV, extracts words from a specified text column, 
    and counts word occurrences for each row.
    """
    def __init__(self, csv_path, text_column):
        """
        Initialize the NormalizedInput object.

        Args:
            csv_path (str): Path to the CSV file.
            text_column (str): Name of the column containing text to process.
        """
        self.csv_path = csv_path
        self.text_column = text_column
        self.df = None
        self.processed_df = None

    def read_csv(self):
        """
        Reads the CSV file into a pandas DataFrame.
        """
        self.df = pd.read_csv(self.csv_path)

    def normalize_text(self, text):
        """
        Converts text to lowercase and extracts words using regex.

        Args:
            text (str): The input text to normalize.

        Returns:
            list: A list of lowercase words extracted from the text.
        """
        words = re.findall(r'\b[a-zA-Z]+\b', str(text).lower())
        return words

    def count_words(self, words):
        """
        Counts the occurrences of each word in a list.

        Args:
            words (list): List of words.

        Returns:
            dict: Dictionary with words as keys and their counts as values.
        """
        return dict(Counter(words))

    def process(self):
        """
        Processes the DataFrame by normalizing text and counting word occurrences
        for each row in the specified text column. Stores the result in processed_df.
        """
        if self.df is None:
            self.read_csv()
        print("Original DataFrame:")
        print(self.df)  # Show original DataFrame
        word_counts = []
        for idx, row in self.df.iterrows():
            words = self.normalize_text(row[self.text_column])
            print(f"\nRow {idx} words:", words)
            word_count = self.count_words(words)
            print(f"Row {idx} word count:", word_count)
            word_counts.append(word_count)
        df_counts = pd.DataFrame(word_counts).fillna(0).astype(int)
        df_counts.index = self.df.index  # Ensure index matches original DataFrame
        print("\nProcessed DataFrame (word counts):")
        print(df_counts)  # Show processed DataFrame
        self.processed_df = df_counts

    def get_processed_dataframe(self):
        """
        Returns the processed DataFrame with word counts.
        If not already processed, it will process the data first.

        Returns:
            pandas.DataFrame: DataFrame with word counts for each row.
        """
        if self.processed_df is None:
            self.process()
        return self.processed_df

# ----------------- TemplatesGeneration Class -----------------
import spacy
from spacy.tokens import Doc
from itertools import product

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

POS_CATEGORIES = {
    'VERB': 'verb',
    'NOUN': 'noun',
    'ADJ': 'adjective',
    'ADV': 'adverb',
    'ADP': 'preposition',
    'CCONJ': 'conjunction',
    'DET': 'determiner',
    'PRON': 'pronoun'
}

AMBIGUOUS_WORDS = {
    'drive': ['noun', 'verb'],
    'sing': ['noun', 'verb'],
    'cheer': ['noun', 'verb'],
    'sleep': ['noun', 'verb'],
    'jump': ['noun', 'verb'],
    'bake': ['noun', 'verb'],
    'laugh': ['noun', 'verb'],
    'wish': ['noun', 'verb'],
    'eat': ['noun', 'verb'],
    'unwrap': ['noun', 'verb', 'adjective'],
    # Add more as needed...
}

TEMPLATES = [
    ['determiner', 'adjective', 'noun', 'verb', 'preposition', 'determiner', 'noun'],
    ['determiner', 'adjective', 'noun'],
    ['determiner', 'noun', 'verb', 'noun'],
    ['noun', 'verb', 'noun'],
    ['determiner', 'noun'],
    ['noun', 'verb'],
    ['noun', 'noun'],
]

FALLBACK_TEMPLATES = [
    ['noun', 'verb', 'noun'],
    ['determiner', 'noun'],
    ['noun', 'verb'],
    ['noun', 'noun'],
]

class TemplatesGeneration:
    def __init__(self, csv_path, text_column):
        self.csv_path = csv_path
        self.text_column = text_column
        self.df = pd.read_csv(csv_path)
        self.all_sentences = []

    def classify_words_in_row(self, row):
        words = re.findall(r'\b[a-zA-Z]+\b', str(row[self.text_column]).lower())
        doc = Doc(nlp.vocab, words=words)
        for name, proc in nlp.pipeline:
            doc = proc(doc)
        results = []
        for token in doc:
            pos_list = [POS_CATEGORIES.get(token.pos_, token.pos_.lower())]
            if token.text in AMBIGUOUS_WORDS:
                for amb_pos in AMBIGUOUS_WORDS[token.text]:
                    if amb_pos not in pos_list:
                        pos_list.append(amb_pos)
            results.append({'id': row['id'], 'word': token.text, 'pos_list': pos_list})
        return results

    def group_words_by_pos(self, classified_words):
        grouped = {cat: [] for cat in POS_CATEGORIES.values()}
        for item in classified_words:
            for pos in item['pos_list']:
                if pos in grouped and item['word'] not in grouped[pos]:
                    grouped[pos].append(item['word'])
        return grouped

    def generate_sentences_for_template(self, word_pos_dict, template):
        if all(word_pos_dict.get(pos) for pos in template):
            return [' '.join(words) for words in product(*(word_pos_dict[pos] for pos in template))]
        return []

    def get_largest_template(self, word_pos_dict):
        for template in TEMPLATES:
            if all(word_pos_dict.get(pos) for pos in template):
                return template
        return None

    def get_unused_words(self, all_words, used_words):
        return set(all_words) - set(used_words)

    def generate(self):
        for _, row in self.df.iterrows():
            classified = self.classify_words_in_row(row)
            word_pos_dict = self.group_words_by_pos(classified)
            all_words = [item['word'] for item in classified]
            largest_template = self.get_largest_template(word_pos_dict)
            used_words = set()
            generated_sentences = []

            if largest_template:
                generated_sentences = self.generate_sentences_for_template(word_pos_dict, largest_template)
                for sentence in generated_sentences:
                    used_words.update(sentence.split())

            unused_words = self.get_unused_words(all_words, used_words)
            if unused_words:
                unused_word_pos_dict = {cat: [w for w in word_pos_dict[cat] if w in unused_words] for cat in word_pos_dict}
                for template in FALLBACK_TEMPLATES:
                    fallback_sentences = self.generate_sentences_for_template(unused_word_pos_dict, template)
                    for sentence in fallback_sentences:
                        words_in_sentence = set(sentence.split())
                        if words_in_sentence & unused_words:
                            generated_sentences.append(sentence)
                            used_words.update(words_in_sentence)
                    unused_words = self.get_unused_words(all_words, used_words)
                    if not unused_words:
                        break

            for sentence in generated_sentences:
                self.all_sentences.append({'id': row['id'], 'sentence': sentence})

        sentences_df = pd.DataFrame(self.all_sentences)
        sentences_df.to_csv("sentence_generation.csv", index=False)
        print("All generated sentences saved to sentence_generation.csv")

# ----------------- Main -----------------
if __name__ == "__main__":
    """
    Example usage of the NormalizedInput class.
    Reads a CSV file, processes the text column, and prints the word counts.
    """
    csv_path = 'test_cases.csv'
    text_column = 'text' 
    # Normalization and word count
    ni = NormalizedInput(csv_path, text_column)  
    ni.read_csv()
    ni.process()
    df = ni.get_processed_dataframe()
    print(df)
    # Template generation and saving
    tg = TemplatesGeneration(csv_path, text_column)
    tg.generate()
