## CS547 Group Project - Musical Search Engine Recommender Using TF_IDF and Sentiment Analysis
Welcome to the Search Engine! Given a set of filters and search options, our project intends to display songs that best match the search result. This will help new music listeners to choose songs that best match a specific emotion or term they associate with

[Link to github repository](https://github.com/vagmi20/ds547project_2025)

[Link to project dataset](https://www.kaggle.com/datasets/carlosgdcj/genius-song-lyrics-with-language-information/data)

[Link to playlist Songs dataset](https://www.kaggle.com/datasets/himanshuwagh/spotify-million/data)

## Dependencies and Startup

Create and activate environment with python version
Mac:
```
python3 -m venv my-env
source my-env/bin/activate
```

Windows:
```
python -m venv my-env
my-env\Scripts\activate
```

Install dependencies

```
pip install -r requirements.txt
```

Run the application
```
streamlit run main.py
```
Username is admin, password is admin123











## About Project

## NLP Processing 
Our project contains scripts that convert a subset into an SQL DB, which would later be used for querying. 

Notes:
- The processor uses NLTK (stopwords + Snowball stemmer) and removes accents by default for IR.
## Sentiment Analysis
- Based on the song lyrics data, we perform sentiment analysis to the lyrics and add the sentiment to a column in the database



# Process Songs:
Edit the config.py file and add the variables:
    - SONG_CSV_PATH ='path to the csv file'
    - INDEX_PATH = 'path to the tfidf index joblib file'

NLP preprocessing to create a tf-idf index over the lyric tokens:
```
python process_songs.py 
```
## Sentiment Analysis
- Use NLTK's SentimentIntensityAnalyzer class to perform sentiment analysis on the lyrics for each song in the DB
- The computed sentiment is added to a column in the DB which is later used for ranking songs based on sentiment


# Playlist Metadata
Download the spotify million playlist from kaggle(link above)
use the utils/playlist_metadata.py to create playlist metadata file
usage:
```
python playlist_metadata.py --spotify-dir 'path to spotify data dir' \
                            --genius-csv 'path to song lyrics csv' \
                            --output 'output file location'
```
Demo playlist search:
playlist_search.find_playlist(query, config)


## Demo
In order to access the music engine, please make sure to follow the steps above in terms of Dependencies and Data. 


## Limitations
- Expensive Overhead
    - Tokenize and Analyze Query, Scrape Lyrics that best match query, display results in format, etc. These can be computationally expensive
- Static Application
    - Unable to dynamically monitor for new and upcoming songs, can be solved with a backend cache or constantly updating server
- Limited Recommender
    - Each Search Result is Independent of Another, does not account for user search history


## Conclusions and Future Work
- Built a holistic and efficient tool that utilizes IR concepts in best recommending music given filters and search options 
- Cloud Storage Handling
    - Some form of DB that lives behind the application
    - Learns from prior searches by other users of the tool
- Incorporate a form of audio processing for improved evaluation measures 
