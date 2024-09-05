from sqlalchemy import create_engine
from movie_app_db import Base

def create_database():
    # Create an SQLite engine
    engine = create_engine('sqlite:///movie_app.db')

    # Create all tables in the database
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_database()
