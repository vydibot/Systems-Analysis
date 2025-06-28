import pandas as pd
import re
from collections import Counter

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
        for each row in the specified text column. Stores the result as a dict
        mapping row id to a dict of word counts.
        """
        if self.df is None:
            self.read_csv()
        print("Original DataFrame:")
        print(self.df)  # Show original DataFrame
        processed_dict = {}
        for idx, row in self.df.iterrows():
            words = self.normalize_text(row[self.text_column])
            print(f"\nRow {idx} words:", words)
            word_count = self.count_words(words)
            print(f"Row {idx} word count:", word_count)
            # Use the row's 'id' as the key if it exists, otherwise use idx
            row_id = row['id'] if 'id' in row else idx
            processed_dict[row_id] = word_count
        print("\nProcessed dict (id -> word counts):")
        print(processed_dict)
        self.processed_df = processed_dict

    def get_processed_dataframe(self):
        """
        Returns the processed dictionary with word counts per id.
        If not already processed, it will process the data first.

        Returns:
            dict: Dictionary mapping id to word count dict.
        """
        if self.processed_df is None:
            self.process()
        return self.processed_df
