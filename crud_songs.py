from sqlmodel import Session, select
from models import MusicDB
from schemas_songs import *

def create_song_entry(sess : Session, song : CreateSongEntry):
    sess.add(song)
    sess.commit()
    sess.refresh(song)

    return song

def update_song_entry(sess : Session, song_id : int, song : UpdateSongEntry):
    existing_song_entry = sess.get(MusicDB, song_id)

    if existing_song_entry is None:
        return None

    if song.file_name is not None:
        existing_song_entry.file_name = song.file_name

    if song.song_name is not None:
        existing_song_entry.song_name = song.song_name

    if song.artist is not None:
        existing_song_entry.artist = song.artist

    if song.file_path is not None:
        existing_song_entry.file_path = song.file_path

    if song.lyrics is not None:
        existing_song_entry.lyrics = song.lyrics

    sess.add(existing_song_entry)
    sess.commit()
    sess.refresh(existing_song_entry)

    return existing_song_entry

def get_song_entry(sess : Session, song_entry_name : str):
    statement = select(MusicDB).where(MusicDB.song_name == song_entry_name)
    results = sess.exec(statement)

    list_of_songs = []
    for song in results:
        list_of_songs.append(song)

    return list_of_songs

def get_all_songs(sess : Session):
    return sess.exec(select(MusicDB)).all()

def delete_song_entry(sess : Session, song_entry_id : int):
    song = sess.get(MusicDB, song_entry_id)

    if song is None:
        return None

    sess.delete(song)
    sess.commit()

    return song