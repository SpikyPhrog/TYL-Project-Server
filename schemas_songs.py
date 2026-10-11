from sqlmodel import SQLModel

class CreateSongEntry(SQLModel):
    file_name : str
    song_name : str
    artist : str
    file_path : str
    lyrics : str

class UpdateSongEntry(SQLModel):
    file_name : str | None
    song_name : str | None
    artist : str | None
    file_path : str | None
    lyrics : str | None

class ReadSongEntry(SQLModel):
    id : int
    file_name: str
    song_name: str
    artist: str
    file_path: str
    lyrics: str