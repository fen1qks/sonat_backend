import requests
from ytmusicapi import YTMusic

from sonat_app.spotifyToken import get_spotify_token

ytmusic = YTMusic()

def search_youtube(search_value):
    items = ytmusic.search(search_value, filter="songs", limit=4)

    tracks = []

    for item in items:
        tracks.append({
            'id': item.get('videoId'),
            'title': item.get('title'),
            'author': ', '.join(
                artist['name'] for artist in item.get('artists',[])
            ),
            'cover': item.get('thumbnails', [{}])[-1].get('url',''),
            'sourceId': item.get('videoId'),
            'watchUrl': f"https://www.youtube.com/watch?v={item.get('videoId')}",
            'searchType':f"youtube",
        })

    return tracks

def search_spotify(search_value):
    token = get_spotify_token()

    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers={
            "Authorization": f"Bearer {token}",
        },
        params={
            "q": search_value,
            "type": "track",
            "limit": 4,
        },
        timeout=10,
    )

    data = response.json()
    tracks = []

    for item in data["tracks"]["items"]:
        tracks.append(
            {
                "id": item["id"],
                "title": item["name"],
                "author": ", ".join(artist["name"] for artist in item["artists"]),
                "cover": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
                "sourceId": item["id"],
                "watchUrl": item["external_urls"]["spotify"],
                "sourceType":"spotify"
            }
        )

    return tracks
