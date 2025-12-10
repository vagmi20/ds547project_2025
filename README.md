## CS547 Group Project - Musical Search Engine Recommender Using TF_IDF and Sentiment Analysis
Welcome to the Search Engine! Given a set of filters and search options, our project intends to display songs that best match the search result. This will help new music listeners to choose songs that best match a specific emotion or term they associate with

## Dependencies and Startup

Create and activate environment with python version
```
python3 -m venv my-env
source my-env/bin/activate
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

## Data
Given the high computational overhead and limited resources, we aimed to deploy a subset of songs (up to 300,000) and rather develop a proof-of-concept using Information Retrieval tools. We utilized the following link:

```
https://www.kaggle.com/datasets/carlosgdcj/genius-song-lyrics-with-language-information/data 
```

After downloading and unzipping the CSV, the recommended step is to take a subset and move into the data/ folder of the repo. The easiest way is to take the first 2,000,000 lines. 
```
head {number} data/song_lyrics.csv > data/song_lyrics_subset.csv
```

Our project contains scripts that convert a subset into an SQL DB, which would later be used for querying. 

## TF_IDF (with Multiple Languages)

## Sentiment Analysis


## Demo
In order to access the music engine, please make sure to follow the steps above in terms of Dependencies and Data. 


## Acknowledgements
We would like to thank Professor and the TA for their guidance during the semester.
