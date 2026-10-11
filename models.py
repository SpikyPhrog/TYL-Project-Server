from sqlmodel import Field, SQLModel
from sqlalchemy import TEXT, Column

class Challenge(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    english_name : str
    bulgarian_name : str
    emoji : str | None = None

class MusicDB(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    file_name : str
    song_name : str
    artist : str
    file_path : str
    lyrics : str = Field(sa_column = Column(TEXT))