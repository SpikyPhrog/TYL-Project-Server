from sqlmodel import SQLModel

class CreateChallenge(SQLModel):
    english_name : str
    bulgarian_name : str
    image_path_key : str | None

class UpdateChallenge(SQLModel):
    english_name: str | None
    bulgarian_name: str | None
    image_path_key: str | None

class ReadChallenge(SQLModel):
    id : int
    english_name: str
    bulgarian_name: str
    image_path_key: str | None = None


