import os
from sqlmodel import create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DatabaseURL")

if DATABASE_URL is not None:
    engine = create_engine(DATABASE_URL, echo = True, pool_pre_ping = True, pool_recycle = 1800)
else:
    print("DATABASE URL IS NONE???")
