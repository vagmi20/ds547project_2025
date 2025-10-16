import scrapy
import bs4 as BeautifulSoup
import requests
import re

def get_top_songs_from_genius(artist_query, max_songs=10):
    base_url = "https://genius.com"
    search_url = f"{base_url}/api/search/multi?per_page=5&q={artist_query.replace(' ', '%20')}"
    response = requests.get(search_url)
    if response.status_code != 200:
        print(f"Failed to retrieve search results for {artist_query}: Status code {response.status_code}")
        return []

    data = response.json()
    song_urls = []
    for section in data.get('response', {}).get('sections', []):
        if section.get('type') == 'song':
            for hit in section.get('hits', []):
                song_url = hit.get('result', {}).get('url')
                if song_url:
                    song_urls.append(song_url)
                    if len(song_urls) >= max_songs:
                        print("breaking..")
                        break
        if len(song_urls) >= max_songs:
            break

    return song_urls

def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}: Status code {response.status_code}")
            return None

        soup = BeautifulSoup.BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        return text
    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")
        return None

def scrape_multiple_websites(urls):
    all_texts = {}
    for url in urls:
        text = scrape_website(url)
        if text:
            all_texts[url] = text
    return all_texts