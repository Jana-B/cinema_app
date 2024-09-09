from sqlalchemy import create_engine, text
from movie_app_db import Base
from sqlalchemy.orm import Session

def create_database():
    # Create an SQLite engine
    engine = create_engine('sqlite:///movie_app.db')

    # Create all tables in the database
    Base.metadata.create_all(engine)

    # Create the view after the tables are created
    create_movie_full_details_view(engine)

    


def create_movie_full_details_view(engine):
    with engine.connect() as connection:
        create_view_query = """
        CREATE VIEW movie_full_details AS
        SELECT 
            m.movie_id, 
            m.movie_name, 
            m.movie_release_date, 
            m.movie_summary,
            GROUP_CONCAT(DISTINCT p.name) AS credits,
            GROUP_CONCAT(DISTINCT g.genre_name) AS genres,
            GROUP_CONCAT(DISTINCT s.studio_name) AS studios,
            GROUP_CONCAT(DISTINCT k.keyword_name) AS keywords
        FROM movie m
        LEFT JOIN movie_credit mc ON m.movie_id = mc.movie_id
        LEFT JOIN person p ON mc.person_id = p.person_id
        LEFT JOIN movie_genre mg ON m.movie_id = mg.movie_id
        LEFT JOIN genre g ON mg.genre_id = g.genre_id
        LEFT JOIN movie_studio ms ON m.movie_id = ms.movie_id
        LEFT JOIN studio s ON ms.studio_id = s.studio_id
        LEFT JOIN movie_keyword mk ON m.movie_id = mk.movie_id
        LEFT JOIN keyword k ON mk.keyword_id = k.keyword_id
        GROUP BY m.movie_id;
        """
        connection.execute(text(create_view_query))





if __name__ == "__main__":
    create_database()
    
