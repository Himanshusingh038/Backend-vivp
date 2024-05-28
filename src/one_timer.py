import json
import pandas as pd
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import Song

def load_json_to_db():
    # Load JSON data
    with open('playlist.json') as f:
        data = json.load(f)

    transposed_arr = []
    for key in data.keys():
        colm = list(data[key].values())
        transposed_arr.append(colm)
    normalised_arr = list(zip(*transposed_arr))

    # Normalize data
    df = pd.DataFrame(normalised_arr, columns=[key for key in data.keys()])
    session: Session = SessionLocal()
    
    for _, row in df.iterrows():
        # Check if the song already exists
        existing_song = session.query(Song).filter(Song.id == row['id']).first()
        if existing_song:
            # Update the existing record
            existing_song.title = row['title']
            existing_song.danceability = row['danceability']
            existing_song.energy = row['energy']
            existing_song.key = row['key']
            existing_song.loudness = row['loudness']
            existing_song.mode = row['mode']
            existing_song.acousticness = row['acousticness']
            existing_song.instrumentalness = row['instrumentalness']
            existing_song.liveness = row['liveness']
            existing_song.valence = row['valence']
            existing_song.tempo = row['tempo']
            existing_song.duration_ms = row['duration_ms']
            existing_song.time_signature = row['time_signature']
            existing_song.num_bars = row['num_bars']
            existing_song.num_sections = row['num_sections']
            existing_song.num_segments = row['num_segments']
            existing_song.class_ = row['class']
        else:
            # Create a new record
            new_song = Song(
                id=row['id'],
                title=row['title'],
                danceability=row['danceability'],
                energy=row['energy'],
                key=row['key'],
                loudness=row['loudness'],
                mode=row['mode'],
                acousticness=row['acousticness'],
                instrumentalness=row['instrumentalness'],
                liveness=row['liveness'],
                valence=row['valence'],
                tempo=row['tempo'],
                duration_ms=row['duration_ms'],
                time_signature=row['time_signature'],
                num_bars=row['num_bars'],
                num_sections=row['num_sections'],
                num_segments=row['num_segments'],
                class_=row['class']
            )
            session.add(new_song)
    
    session.commit()
    session.close()
