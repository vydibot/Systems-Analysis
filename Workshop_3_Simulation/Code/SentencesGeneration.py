import pandas as pd
from collections import Counter

class SentencesGeneration:
    def __init__(self, sentence_csv_path, processed_dict):
        """
        Args:
            sentence_csv_path (str): Path to templates_generation.csv (from TemplatesGeneration)
            processed_dict (dict): {row_id: {word: count, ...}, ...} from NormalizedInput
        """
        self.sentence_csv_path = sentence_csv_path
        self.processed_dict = processed_dict
        self.sent_df = pd.read_csv(sentence_csv_path)
        self.final_sentences = []

    def combine_sentences_per_row(self):
        for row_id, word_count_dict in self.processed_dict.items():
            original_bag = []
            for word, count in word_count_dict.items():
                original_bag.extend([word] * count)
            original_counter = Counter(original_bag)
            n_words = len(original_bag)

            row_sentences = self.sent_df[self.sent_df['id'] == row_id]['sentence'].tolist()
            sentence_word_lists = [s.split() for s in row_sentences]

            used_counter = Counter()
            selected_sentences = []
            for words, sent in sorted(zip(sentence_word_lists, row_sentences), key=lambda x: -len(x[0])):
                temp_counter = Counter(words)
                if all(used_counter[w] + temp_counter[w] <= original_counter[w] for w in temp_counter):
                    selected_sentences.append(sent)
                    used_counter += temp_counter
                if sum(used_counter.values()) == n_words:
                    break

            if sum(used_counter.values()) < n_words:
                print(f"Warning: Could not cover all words for row {row_id}.")

            self.final_sentences.append({
                "id": row_id,
                "combined_sentence": " ".join(selected_sentences)
            })

    def save(self, output_path="sentences_generation.csv"):
        pd.DataFrame(self.final_sentences).to_csv(output_path, index=False)
        print(f"Combined sentences saved to {output_path}")
