from sqlmodel import Session, select
from models import Challenge
from schemas_challenges import *

def create_challenge(session: Session, challenge : CreateChallenge):
    session.add(challenge)
    session.commit()
    session.refresh(challenge)

    return challenge

def update_challenge(session : Session, challenge_id : int, challenge : UpdateChallenge):
    existing_challenge = session.get(Challenge, challenge_id)

    if existing_challenge is None:
        return None

    if challenge.english_name is not None:
        existing_challenge.english_name = challenge.english_name

    if challenge.bulgarian_name is not None:
        existing_challenge.bulgarian_name = challenge.bulgarian_name

    if challenge.image_path_key is not None:
        existing_challenge.image_path_key = challenge.image_path_key

    session.add(existing_challenge)
    session.commit()
    session.refresh(existing_challenge)

    return existing_challenge

def get_challenge(session : Session, challenge_id : int):
    challenge = session.get(Challenge, challenge_id)

    return challenge

def get_challenges(session : Session):
    return session.exec(select(Challenge)).all()

def delete_challenge(session : Session, challenge_id : int):
    challenge = session.get(Challenge, challenge_id)

    if challenge is None:
        return None

    session.delete(challenge)
    session.commit()

    return challenge