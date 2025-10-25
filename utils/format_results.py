## Given a JSON object filled with links, format it as a pretty-printed string
## Return as a string with image, song names, and otther details
import json

# given a genius url, display the song name, image (from the url), and artist name
def get_results(url):
    try:
        parts = url.split('/')
        artist = parts[3].replace('-', ' ').title()
        song = parts[4].replace('-', ' ').title()
        image_url = f"https://images.genius.com/{parts[5]}.jpg"
        return {
            "artist": artist,
            "song": song,
            "image_url": image_url
        }
    except IndexError:
        return None

def format_results(json_data):
    try:
        data = json.loads(json_data)
        results = []
        for item in data.get('results', []):
            url = item.get('url')
            if url:
                result = get_results(url)
                if result:
                    results.append(result)
        
        formatted_string = ""
        for res in results:
            formatted_string += f"Artist: {res['artist']}\n"
            formatted_string += f"Song: {res['song']}\n"
            formatted_string += f"Image URL: {res['image_url']}\n\n"
        
        return formatted_string.strip()
    except json.JSONDecodeError:
        return "Invalid JSON data."