import crud_challenges
import crud_songs
from fastapi import FastAPI, HTTPException, Form, WebSocket, WebSocketDisconnect
from sqlmodel import Session
from database import engine
# from schemas_challenges import *
from schemas_songs import *
from RadioControls.radioAPI import *
from contextlib import asynccontextmanager

SQLModel.metadata.create_all(engine)
radio = RadioTelnetManager()

connected_clients = set()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await radio.connect()

    yield

    await radio.close()

app = FastAPI(lifespan = lifespan)

current_track = {
    "artist" : "",
    "title" : ""
}

@app.get("/")
def read_root():
    return {"Hello" : "World"}


@app.websocket("/ws/radio")
async def radio_websocket(websocket : WebSocket):
    await websocket.accept()
    print("Websocket accepted")
    connected_clients.add(websocket)
    try:
        while True:
            message = await websocket.receive_json()

            action = message.get("action")

            if action == "skip":
                await radio.skip()

                await websocket.send_json(
                    {
                        "type" : "command_result",
                        "action" : "skip",
                        "status" : "ok"
                    }
                )
            elif action == "get_currently_playing":
                track = await radio.currently_playing()

                await websocket.send_json(
                    {
                        "type": "now_playing",
                        "data" : track
                    }
                )
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast(message : dict):
    dead_clients = []

    for client in connected_clients:
        try:
            await client.send_json(message)
        except Exception:
            dead_clients.append(client)

    for client in dead_clients:
        connected_clients.discard(client)

async def broadcast_track():
    message = {
        "type" : "now_playing",
        "data" : current_track
    }
    await broadcast(message)

@app.get("/challenges/{challenge_id}")
def get_challenge(challenge_id : int):
    with Session(engine) as session:
        challenge = crud_challenges.get_challenge(session, challenge_id)

        if challenge is None:
            raise HTTPException(
                status_code = 404,
                detail = "Challenge not found"
            )

        return challenge

@app.get("/challenges")
def get_challenges():
    with Session(engine) as session:
        return crud_challenges.get_challenges(session)

@app.post("/track")
async def post_track(artist : str = Form(...), title : str = Form(...)):
    current_track["artist"] = artist
    current_track["title"] = title

    await broadcast_track()

    return {"status" : "ok"}


@app.get("/radio/track")
def get_track():
    return current_track

@app.get("/song/{songName}")
def get_song(songName : str):
    with Session(engine) as session:
        song = crud_songs.get_song_entry(session, songName)

        if song is None:
            raise HTTPException(
                status_code = 404,
                detail = "Song not found"
            )

        return song

@app.post("/song/add", response_model = ReadSongEntry)
def create_song_entry(song : CreateSongEntry):
    with Session(engine) as session:
        return crud_songs.create_song_entry(session, song)


# @app.delete("/song/delete/{songID}")
# def delete_song(songID : int):
#     with Session(engine) as session:
#         song = crud_songs.delete_song_entry(session, songID)
#
#         if song is None:
#             raise HTTPException(
#                 status_code = 404,
#                 detail = "Song Not Found"
#             )
#
#         return song

#
# @app.post("/challenges", response_model = ReadChallenge)
# def create_challenge(challenge : CreateChallenge):
#     with Session(engine) as session:
#         return crud.create_challenge(session, challenge)
#
# @app.put("/challenges/{challenge_id}")
# def update_challenge(challenge_id : int, challenge : UpdateChallenge):
#     with Session(engine) as session:
#         existing_challenge = crud.update_challenge(session, challenge_id, challenge)
#
#         if existing_challenge is None:
#             raise HTTPException(
#                 status_code = 404,
#                 detail = "Not found"
#             )
#
#         return existing_challenge
#
# @app.delete("/challenges/{challenge_id}")
# def delete_challenge(challenge_id : int):
#     with Session(engine) as session:
#         challenge_to_delete = crud.delete_challenge(session, challenge_id)
#
#         if challenge_to_delete is None:
#             raise HTTPException(
#                 status_code = 404,
#                 detail = "Not found"
#             )
#
#         return challenge_to_delete