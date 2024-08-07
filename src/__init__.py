from dotenv import load_dotenv

from src.database.databaseinitiator import DatabaseInitiator

load_dotenv(override=True)

with DatabaseInitiator() as db:
    db.init_db()
