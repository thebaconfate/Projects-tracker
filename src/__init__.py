import os
from dotenv import load_dotenv

from src.database.databaseinitiator import DatabaseInitiator

load_dotenv(override=True)

TESTING = os.getenv("TESTING")
if not TESTING:
    with DatabaseInitiator() as db:
        db.init_db()
