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
        self.df = pd.read_csv(self.csv_path)

    def normalize_text(self, text):
        # Lowercase and split into words
        words = re.findall(r'\b[a-zA-Z]+\b', str(text).lower())
        return words

    def count_words(self, words):
        # Count occurrences of each word
        return dict(Counter(words))

    def process(self):
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
        if self.processed_df is None:
            self.process()
        return self.processed_df

if __name__ == "__main__":
    csv_path = 'sample_submission.csv'
    text_column = 'text' 
    ni = NormalizedInput(csv_path, text_column)  
    ni.read_csv()
    ni.process()
    df = ni.get_processed_dataframe()
    print(df)


