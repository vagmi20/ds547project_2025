import pandas as pd
import os
import json
from collections import defaultdict


class PlaylistMetadataBuilder:
    
    def __init__(self, spotify_data_dir):
        self.spotify_data_dir = spotify_data_dir
        self.playlist_song_map = defaultdict(list)
        self.song_playlist_map = defaultdict(list)
        
    def load_spotify_playlists(self):
        # Find all JSON files in the directory
        json_files = [f for f in os.listdir(self.spotify_data_dir) if f.endswith('.json')]
        
        all_rows = []
        for json_file in json_files:
            print(f"Loading {json_file}...")
            with open(os.path.join(self.spotify_data_dir, json_file), 'r') as f:
                data = json.load(f)
                
            # Parse playlists
            for playlist in data.get('playlists', []):
                playlist_name = playlist.get('name', '')
                playlist_desc = playlist.get('description', '')
                
                for track in playlist.get('tracks', []):
                    all_rows.append({
                        'playlist_name': playlist_name,
                        'playlist_description': playlist_desc,
                        'track_name': track.get('track_name', ''),
                        'artist_name': track.get('artist_name', ''),
                        'album_name': track.get('album_name', ''),
                        'duration_ms': track.get('duration_ms', 0)
                    })
        
        if all_rows:
            return pd.DataFrame(all_rows)
        return pd.DataFrame()
    
    def build_metadata(self, genius_csv_path, output_path, chunk_size=100000):
        # Load Genius data 
        print("Loading Genius lyrics data...")
        genius_df = pd.read_csv(genius_csv_path, usecols=['title', 'artist'])
        print(f"Loaded {len(genius_df)} songs from Genius")
        
        genius_df['title_lower'] = genius_df['title'].astype(str).str.lower().str.strip()
        genius_df['artist_lower'] = genius_df['artist'].astype(str).str.lower().str.strip()
        genius_df['song_key'] = genius_df['title'] + '|' + genius_df['artist']
        
        # Create a set of normalized genius songs for fast lookup
        genius_lookup = set(zip(genius_df['title_lower'], genius_df['artist_lower']))
        genius_key_map = dict(zip(zip(genius_df['title_lower'], genius_df['artist_lower']), genius_df['song_key']))
        
        print(f"created lookup index for {len(genius_lookup)} unique songs")
    
        song_playlists = defaultdict(set)
        song_tags = defaultdict(set)
        
        json_files = sorted([f for f in os.listdir(self.spotify_data_dir) if f.endswith('.json')])
        total_processed = 0
        matched_songs = set()
        
        for json_file in json_files:
            print(f"\nProcessing {json_file}...")
            with open(os.path.join(self.spotify_data_dir, json_file), 'r') as f:
                data = json.load(f)
            for playlist in data.get('playlists', []):
                playlist_name = playlist.get('name', '')
                playlist_desc = playlist.get('description', '')
                tags = self._extract_tags(playlist_name)
                if playlist_desc:
                    tags.update(self._extract_tags(playlist_desc))
                
                for track in playlist.get('tracks', []):
                    total_processed += 1
                    track_lower = track.get('track_name', '').lower().strip()
                    artist_lower = track.get('artist_name', '').lower().strip()
                    
                    lookup_key = (track_lower, artist_lower) # checks if a song is in the genius lookup
                    if lookup_key in genius_lookup:
                        song_key = genius_key_map[lookup_key]
                        song_playlists[song_key].add(playlist_name)
                        song_tags[song_key].update(tags)
                        matched_songs.add(song_key)
                    
                    if total_processed % 100000 == 0:
                        print(f"  Processed {total_processed} tracks, matched {len(matched_songs)} songs")
        
        print(f"Total Spotify tracks processed: {total_processed}")
        print(f"Matched {len(matched_songs)} songs between spotify and genius")
        
        metadata_rows = []
        for song_key in matched_songs:
            title, artist = song_key.split('|', 1)
            playlists = song_playlists[song_key]
            metadata_rows.append({
                'title': title,
                'artist': artist,
                'playlists': '|'.join(playlists),
                'playlist_count': len(playlists),
                'tags': '|'.join(song_tags[song_key])
            })
        
        metadata_df = pd.DataFrame(metadata_rows)
        metadata_df.to_csv(output_path, index=False)
        print(f"Saved playlist metadata to {output_path}")
        print(f"Total songs with playlist data: {len(metadata_df)}")
        return metadata_df
    
    def _extract_tags(self, playlist_name):
        keywords = ['club', 'party', 'workout', 'chill', 'dance', 'frat', 
                   'edm', 'hype', 'study', 'relax', 'summer', 'rap', 'pop']
        tags = set()
        name_lower = playlist_name.lower()
        
        for keyword in keywords:
            if keyword in name_lower:
                tags.add(keyword)
        
        #extract year if present
        import re
        years = re.findall(r'\b(20\d{2})\b', playlist_name)
        tags.update(years)
        
        return tags


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--spotify-dir', required=True, help='Spotify playlist dir')
    parser.add_argument('--genius-csv', required=True, help='Path to tfidf csv file')
    parser.add_argument('--output', required=True, help='Output path for playlist metadata')
    args = parser.parse_args()
    
    builder = PlaylistMetadataBuilder(args.spotify_dir)
    builder.build_metadata(args.genius_csv, args.output)
