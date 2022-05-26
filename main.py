import tekore as tk
from dotenv import load_dotenv
import os
import sqlite3

def find_playlists_containing_track(followed_playlists, track):
    found_playlists = []
    for playlist in followed_playlists:
        playlist_items = list(map(lambda item: item.track, spotify.playlist_items(playlist_id=playlist.id).items))
        if track in playlist_items:
            found_playlists.append(track)
    return found_playlists

# get bot credentials
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# authorise tekore
tk_config = 'tekore.cfg'
token = None
try:
    conf = tk.config_from_file(tk_config, return_refresh=True)
    token = tk.refresh_user_token(*conf[:2], conf[3])
except:
    redirect_uri = 'https://example.com/callback'
    token = tk.prompt_for_user_token(client_id, client_secret, redirect_uri, scope=tk.scope.every)
    conf = (client_id, client_secret, redirect_uri, token.refresh_token)
    tk.config_to_file(tk_config, conf + (token.refresh_token,))

spotify = tk.Spotify(token)

# establish db connection and create table if needed
con = sqlite3.connect('neton.db')
db_cur = con.cursor()
table_name = "playlist_tracks_" + spotify.current_user().id
print(table_name)
db_cur.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' and name='{table_name}'")
if db_cur.fetchone()[0] != 1:
    db_cur.execute(f"CREATE TABLE {table_name} (row_id INTEGER PRIMARY KEY AUTOINCREMENT, track text NOT NULL, artists text NOT NULL)")

# iterate through playlists
followed_playlists = spotify.all_items(spotify.followed_playlists())
saved_tracks_page = spotify.saved_tracks()

end = False
while saved_tracks_page != None:
    saved_tracks = saved_tracks_page.items
    for track in saved_tracks:
        playlists = find_playlists_containing_track(followed_playlists, track)
        print(f"{track.track.name} found in:")
        for playlist in playlists:
            print(playlist.name)
        user_input = input("Continue? [Y/n]")
        if user_input == "y" or user_input == "Y":
            continue
        else:
           end = True
           break
    if end:
        break
    spotify.next(saved_tracks_page)
