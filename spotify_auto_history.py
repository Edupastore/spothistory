import os
import pandas as pd
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# ---------------------- Configuración desde secrets ----------------------
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
CACHE_CONTENT = os.getenv("SPOTIPY_CACHE")  # token guardado en secret
DATA_PATH = "spotify_history.csv"
CACHE_PATH = ".cache"

# ---------------------- Crear archivo .cache si no existe ----------------------
if CACHE_CONTENT and not os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "w") as f:
        f.write(CACHE_CONTENT)

# ---------------------- Conexión a Spotify ----------------------
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-recently-played",
    cache_path=CACHE_PATH,
    open_browser=False
))

# ---------------------- Obtener últimas 50 reproducciones ----------------------
data = sp.current_user_recently_played(limit=50)
items = data.get("items", [])

rows = []

for item in items:
    track = item["track"]
    album = track["album"]
    artist = track["artists"][0]

    # --------- Llamadas extra a la API ---------
    artist_full = sp.artist(artist["id"])

    rows.append({
        # Reproducción
        "played_at": item["played_at"],

        # Track
        "track_name": track["name"],
        "track_id": track["id"],
        "duration_ms": track["duration_ms"],

        # Artist
        "artist_name": artist["name"],
        "artist_id": artist["id"],
        "artist_genres": ", ".join(artist_full.get("genres", [])),
        artist_images = artist_full.get("images", [])
        artist_img = artist_images[1]["url"] if len(artist_images) > 1 else (artist_images[0]["url"] if artist_images else None)

        "artist_img": artist_img,

        # Album
        "album_name": album["name"],
        "album_id": album["id"],
        "album_release_year": album.get("release_date", "")[:4],
        "album_label": album.get("label"),
        album_images = album.get("images", [])
        album_img = album_images[1]["url"] if len(album_images) > 1 else (album_images[0]["url"] if album_images else None)

        "album_img": album_img
    })

df_new = pd.DataFrame(rows)

# ---------------------- Guardar histórico sin duplicados ----------------------
if os.path.exists(DATA_PATH):
    df_old = pd.read_csv(DATA_PATH)
    df_total = pd.concat([df_old, df_new]).drop_duplicates(subset=["played_at"])
else:
    df_total = df_new

df_total.sort_values("played_at", inplace=True)
df_total.to_csv(DATA_PATH, index=False)

print(f"Histórico actualizado: {len(df_total)} filas")

