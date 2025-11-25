import os
import pandas as pd
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
CACHE_PATH = ".cache"

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-recently-played",
    cache_path=CACHE_PATH,
    open_browser=False
))

# ----------------------
# Obtener últimas 50 reproducciones
# ----------------------
data = sp.current_user_recently_played(limit=50)
items = data.get("items", [])

rows = []
for item in items:
    track = item["track"]
    rows.append({
        "played_at": item["played_at"],
        "track_name": track["name"],
        "artist": track["artists"][0]["name"],
        "album": track["album"]["name"],
        "duration_ms": track["duration_ms"],
        "track_id": track["id"]
    })

df_new = pd.DataFrame(rows)

# ----------------------
# Guardar histórico sin duplicados
# ----------------------
if os.path.exists(DATA_PATH):
    df_old = pd.read_csv(DATA_PATH)
    df_total = pd.concat([df_old, df_new]).drop_duplicates(subset=["played_at"])
else:
    df_total = df_new

df_total.sort_values("played_at", inplace=True)
df_total.to_csv(DATA_PATH, index=False)

print(f"Histórico actualizado: {len(df_total)} filas")
