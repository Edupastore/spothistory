import pandas as pd
import psycopg2
import os

# ---------------------- Configuración desde secrets de variables de entorno ----------------------
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(
    host="aws-1-eu-north-1.pooler.supabase.com",
    dbname="postgres",
    user="postgres.prwcramdanblevcpaghy",
    password=os.getenv("DB_PASSWORD"),
    port=5432,
    sslmode="require"
)

cur = conn.cursor()

df = pd.read_csv("spotify_history.csv")

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
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (played_at) DO NOTHING;
"""

for _, row in df.iterrows():
    cur.execute(insert_sql, (
        row["played_at"],
        row["track_name"],
        row["duration_ms"],
        row["track_id"],
        row["artist_name"],
        row["artist_id"],
        row["artist_genres"].split(", ") if isinstance(row["artist_genres"], str) else None,
        row["artist_img"],
        row["album_name"],
        row["album_id"],
        row["album_release_year"],
        row["album_label"],
        row["album_img"],
    ))

conn.commit()
cur.close()
conn.close()

print("CSV migrado a Supabase")
