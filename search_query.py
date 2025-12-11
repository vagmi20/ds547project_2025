#simple query search using utils.playlist_search
from utils.playlist_search import find_playlist, search_by_lyrics_and_playlist
query = "house party 2017"
config = {
    'csv_path' : '/home/ostikar/MyProjects/CS547/project/data/genius/song_lyrics.csv',
    'playlist_metadata_path' : '/home/ostikar/MyProjects/CS547/project/data/playlist_metadata.csv',
    'top_k' : 10
    }

playlist = find_playlist(query, config)
for item in playlist:
    print(f"{item['title']} by {item['artist']}")
