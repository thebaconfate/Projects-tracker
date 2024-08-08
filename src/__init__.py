import os
from dotenv import load_dotenv

from src.database import HOST, PORT
from src.database.databaseinitiator import DatabaseInitiator

load_dotenv(override=True)

TESTING = os.getenv("TESTING")
if not TESTING:
    print(PORT, HOST)
    with DatabaseInitiator() as db:
        db.init_db()
