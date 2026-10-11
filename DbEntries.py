from sqlmodel import SQLModel, Session
from database import engine
from models import Challenge, MusicDB

def Entry(challenge : Challenge):
    with Session(engine) as session:
        session.add(challenge)
        session.commit()
        session.refresh(challenge)

# def Entry(song: MusicDB):
#     with Session(engine) as session:
#         session.add(song)
#         session.commit()
#         session.refresh(song)

SQLModel.metadata.create_all(engine)

# Entry(Challenge(english_name="Tiger", bulgarian_name="Тигър", emoji="🐘"))


# #
# Entry(MusicDB(
#     file_name="MYRNE, Aviella-Afterdark (feat. Aviella).mp3", song_name="Afterdark", artist="MYRNE, Aviella",
#     file_path="/home/dark_abyss/Desktop/radio/music/MYRNE, Aviella-Afterdark (feat. Aviella).mp3",
#     lyrics = "I feel so out of line\n \
# Every time that you call my name\n\
# I want to make a move\n\
# But I'm scared to say\n\
# It's taken a while to get this far\n\
# I'm caught and away\n\
# It's taken a ride to get this close\n\
# We're one and the same\n\
# \n\
# Chasing colors after dark\n\
# In your heart, I believe in you\n\
# The way you pull me in\n\
# Can't pretend we’re a work of art\n\
# After dark in your heart\n\
# I believe in you\n\
# The way you pull me in\n\
# Can't pretend I'll be chasing colors\n\
# \n\
# I feel so beautiful when you call\n\
# Tell me we won't change\n\
# I want to make a move\n\
# But I'm scared to say\n\
# It's taken a while to get this far\n\
# I'm caught and away\n\
# It's taken a ride to get this close\n\
# We're one and the same\n\
# \n\
# Chasing colors after dark\n\
# In your heart, I believe in you\n\
# The way you pull me in\n\
# Can't pretend we’re a work of art\n\
# After dark in your heart\n\
# I believe in you\n\
# The way you pull me in\n\
# Can't pretend I'll be chasing colors"))