# app/database.py
import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Item

items = [
    {"id": 1, "name": "Item 1", "description": "Description of Item 1"},
    {"id": 2, "name": "Item 2", "description": "Description of Item 2"},
    {"id": 3, "name": "Item 3", "description": "Description of Item 3"},
]


# Data migration function
def migrate_data_to_database():
    db = SessionLocal()  # Initialize the database session
    try:
        for item_data in items:
            # db_item corresponds to a whole row in the items table
            db_item = Item(**item_data)
            db.add(db_item)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    # Database credentials
    config = configparser.ConfigParser(interpolation=None)
    config.read("../config.ini")
    username = config["fast-api"]["username"]
    password = config["fast-api"]["password"]

    # Connect to Database
    DATABASE_URL = f"postgresql://{username}:{password}@localhost/postgres"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    # Migrate to Database
    migrate_data_to_database()
