from normilizedinput import NormalizedInput
from templatesgeneration import TemplatesGeneration

if __name__ == "__main__":
    csv_path = 'sample_submission.csv'
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
