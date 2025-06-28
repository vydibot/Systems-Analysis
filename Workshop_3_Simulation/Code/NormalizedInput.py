import pandas as pd
import re
from collections import Counter

class NormalizedInput:  
    def __init__(self, csv_path, text_column):
        self.csv_path = csv_path
        self.text_column = text_column
        self.df = None
        self.processed_df = None

    def read_csv(self):
        print("[NormalizedInput] Reading CSV file:", self.csv_path)
        self.df = pd.read_csv(self.csv_path)
        print("[NormalizedInput] CSV loaded. Shape:", self.df.shape)

    def normalize_text(self, text):
        words = re.findall(r'\b[a-zA-Z]+\b', str(text).lower())
        return words

    def count_words(self, words):
        return dict(Counter(words))

    def process(self):
        print("[NormalizedInput] Starting processing of DataFrame.")
        if self.df is None:
            self.read_csv()
        print("Original CSV:")
        print(self.df)
        processed_dict = {}
        for idx, row in self.df.iterrows():
            words = self.normalize_text(row[self.text_column])
            word_count = self.count_words(words)
            row_id = row['id'] if 'id' in row else idx
            processed_dict[row_id] = word_count
        self.processed_df = processed_dict
        print("[NormalizedInput] Processing complete.")

    def get_processed_dictionary(self):
        if self.processed_df is None:
            self.process()
        return self.processed_df

    def get_processed_df(self):
        return self.processed_df
