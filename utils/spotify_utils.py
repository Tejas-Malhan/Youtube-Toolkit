# utils/spotify_utils.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from yt_dlp import YoutubeDL

def extract_titles_from_youtube(playlist_url):
    ydl_opts = {'quiet': True, 'extract_flat': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        return [entry['title'] for entry in info['entries']]

def convert_yt_playlist_to_spotify(yt_url, client_id, client_secret):
    titles = extract_titles_from_youtube(yt_url)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8888/callback/",
        scope="playlist-modify-public playlist-modify-private"
    ))

    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id, "YouTube Converted Playlist", public=True)

    track_uris = []
    for title in titles:
        results = sp.search(q=title, type='track', limit=1)
        tracks = results.get('tracks', {}).get('items', [])
        if tracks:
            track_uris.append(tracks[0]['uri'])

    if track_uris:
        sp.playlist_add_items(playlist['id'], track_uris)

    return playlist['external_urls']['spotify']
