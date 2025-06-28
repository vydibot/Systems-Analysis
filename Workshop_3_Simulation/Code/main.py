from NormalizedInput import NormalizedInput
from TemplatesGeneration import TemplatesGeneration
from SentencesGeneration import SentencesGeneration

if __name__ == "__main__":
    csv_path = 'sample_submission.csv'
    text_column = 'text'
    ni = NormalizedInput(csv_path, text_column)
    processed_dict = ni.get_processed_dictionary()
    tg = TemplatesGeneration(ni)
    tg.generate()  # This writes "templates_generation.csv"
    # processed_dict = ni.get_processed_dictionary()
    sg = SentencesGeneration("templates_generation.csv", processed_dict)
    sg.combine_sentences_per_row()
    sg.save()      # This writes "sentences_generation.csv"
