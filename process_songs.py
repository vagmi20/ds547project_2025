import argparse
import pandas as pd
import os
from language_processing.scripts.lyrics_processor import LyricsProcessor
from utils.sentiment_analysis import analysis
from config import SONG_DATA_PATH, OUTPUT_DIR

def main():

    OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'tfidf_all.csv')
    df = pd.read_csv(SONG_DATA_PATH)
    print(f"Loaded song data")
    processed_rows = []
    for idx, row in df.iterrows():
        print(f"processing: {str(row.get('title'))}")
        lang_code = str(row.get('language_cld3', 'en'))
        if lang_code == 'nan' or not lang_code or lang_code not in LyricsProcessor.lang_map:
            lang_code = 'en'
        processor = LyricsProcessor(language=lang_code, keep_accents=True)
        clean = processor.clean_text(row['lyrics'])
        print(f"    cleaned")
        tokens = processor.tokenize(clean)
        print(f"    tokenized")
        sentiment = analysis(row['lyrics'])['compound']
        print(f"    extracted sentiments")
        new_row = row.to_dict()
        new_row['clean_text'] = ' '.join(tokens)
        new_row['token_count'] = len(tokens)
        new_row['sentiment'] = sentiment
        processed_rows.append(new_row)
    out_df = pd.DataFrame(processed_rows)
    out_df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved processed CSV with sentiment -> {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
