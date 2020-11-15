import tekore as tk
from dotenv import load_dotenv
import os

def find_playlists_containing_track(followed_playlists, track):
    return [playlist for playlist in followed_playlists if track in playlist]

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

conf = (client_id, client_secret, '')
tk_config = 'tekore.cfg'

token = tk.prompt_for_user_token(*conf, tk.scope.every)
tk.config_to_file(tk_config, conf + (token.refresh_token,))

spotify = tk.Spotify(token)
followed_playlists = spotify.all_items(spotify.followed_playlists())
saved_tracks_page = spotify.saved_tracks()

while saved_tracks_page != None:
    saved_tracks = saved_tracks_page.items
    for track in saved_tracks:
        playlists = find_playlists_containing_track(followed_playlists, track)

    spotify.next(saved_tracks_page)