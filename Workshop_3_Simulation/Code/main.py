from NormalizedInput import NormalizedInput
from templatesgeneration import TemplatesGeneration

if __name__ == "__main__":
    csv_path = 'sample_submission.csv'
    text_column = 'text'
    # Normalization and word count
    ni = NormalizedInput(csv_path, text_column)
    processed_dict = ni.get_processed_dictionary()
    print(processed_dict)
    # Template generation and saving
    tg = TemplatesGeneration(ni)
    tg.generate()
