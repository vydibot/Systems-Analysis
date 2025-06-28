import pandas as pd
import re
import spacy
from spacy.tokens import Doc
from itertools import product
import NormalizedInput

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
    def __init__(self, normalized_input):
        self.normalized_input = normalized_input
        self.processed_dict = self.normalized_input.get_processed_dictionary()
        self.all_sentences = []
        self.nlp = spacy.load("en_core_web_sm")

    def classify_words_in_row(self, row_id, words):
        doc = Doc(self.nlp.vocab, words=words)
        for name, proc in self.nlp.pipeline:
            doc = proc(doc)
        results = []
        for token in doc:
            pos_list = [POS_CATEGORIES.get(token.pos_, token.pos_.lower())]
            if token.text in AMBIGUOUS_WORDS:
                for amb_pos in AMBIGUOUS_WORDS[token.text]:
                    if amb_pos not in pos_list:
                        pos_list.append(amb_pos)
            results.append({'id': row_id, 'word': token.text, 'pos_list': pos_list})
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
        for row_id, word_counts in self.processed_dict.items():
            # Reconstruct the normalized words list from word counts
            words = []
            for word, count in word_counts.items():
                words.extend([word] * count)
            classified = self.classify_words_in_row(row_id, words)
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
                self.all_sentences.append({'id': row_id, 'sentence': sentence})

        sentences_df = pd.DataFrame(self.all_sentences)
        sentences_df.to_csv("sentence_generation.csv", index=False)
        print("All generated sentences saved to sentence_generation.csv")
