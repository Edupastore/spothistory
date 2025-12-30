import os
import pandas as pd
import psycopg2
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# ---------------------- Configuración desde secrets de variables de entorno ----------------------
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
CACHE_CONTENT = os.getenv("SPOTIPY_CACHE")
DATABASE_URL = os.getenv("DATABASE_URL")

# ---------------------- Constantes ----------------------

DATA_PATH = "spotify_history.csv"
CACHE_PATH = ".cache"

# ---------------------- Conexión a la base de datos ----------------------

conn = psycopg2.connect(
    host="aws-1-eu-north-1.pooler.supabase.com",
    dbname="postgres",
    user="postgres.prwcramdanblevcpaghy",
    password=os.getenv("DB_PASSWORD"),
    port=5432,
    sslmode="require"
)

cur = conn.cursor()

# ---------------------- Crear archivo .cache si no existe ----------------------
if CACHE_CONTENT and not os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "w") as f:
        f.write(CACHE_CONTENT)

# ---------------------- Conexión a Spotify ----------------------
sp = Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-read-recently-played",
        cache_path=CACHE_PATH,
        open_browser=False,
    )
)

# ---------------------- Obtener últimas 50 reproducciones ----------------------
data = sp.current_user_recently_played(limit=50)
items = data.get("items", [])

rows = []

for item in items:
    track = item["track"]
    album = track["album"]
    artist = track["artists"][0]

    # --------- Llamadas completas ---------
    artist_full = sp.artist(artist["id"])
    album_full = sp.album(album["id"])   # ← NECESARIO para label

    # --------- Imágenes 300x300 ---------
    artist_images = artist_full.get("images", [])
    artist_img = (
        artist_images[1]["url"]
        if len(artist_images) > 1
        else (artist_images[0]["url"] if artist_images else None)
    )

    album_images = album_full.get("images", [])
    album_img = (
        album_images[1]["url"]
        if len(album_images) > 1
        else (album_images[0]["url"] if album_images else None)
    )

    rows.append(
        {
            "played_at": item["played_at"],

            # Track
            "track_name": track["name"],
            "duration_ms": track["duration_ms"],
            "track_id": track["id"],

            # Artist
            "artist_name": artist["name"],
            "artist_id": artist["id"],
            "artist_genres": artist_full.get("genres", None) or None,
            "artist_img": artist_img,

            # Album
            "album_name": album_full.get("name"),
            "album_id": album_full.get("id"),
            "album_release_year": album_full.get("release_date", "")[:4],
            "album_label": album_full.get("label"),
            "album_img": album_img,
        }
    )

# ---------------------- Insert en Postgres ----------------------
insert_sql = """
INSERT INTO spotify_recently_played (
    played_at,
    track_name,
    duration_ms,
    track_id,
    artist_name,
    artist_id,
    artist_genres,
    artist_img,
    album_name,
    album_id,
    album_release_year,
    album_label,
    album_img
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (played_at) DO NOTHING;
"""

for row in rows:
    cur.execute(
        insert_sql,
        (
            row["played_at"],
            row["track_name"],
            row["duration_ms"],
            row["track_id"],
            row["artist_name"],
            row["artist_id"],
            row["artist_genres"],
            row["artist_img"],
            row["album_name"],
            row["album_id"],
            row["album_release_year"],
            row["album_label"],
            row["album_img"],
        )
    )

conn.commit()
cur.close()
conn.close()

print(f"Insertadas {len(rows)} reproducciones (sin duplicados)")

# ---------------------- Conservar una vez para ver si funciona la inserción en la base de datos ----------------------
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
