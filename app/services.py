from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from db.movie_app_db import Movie, MovieGenre, Genre, MovieKeyword, Keyword,\
   MovieCredit, Person, MovieStudio, Studio, MovieDetails
from sqlalchemy import create_engine
import pandas as pd

database_path = 'sqlite:///movie_app.db'

class MovieService:
    def __init__(self):
        # Connect to the SQLite database
        engine = create_engine(database_path)
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    def to_dataframe(self, object_list: list) -> pd.DataFrame: 
          # Convert each object into a dictionary of its attributes
        data = [obj.__dict__ for obj in object_list]

        # Create a pandas DataFrame from the list of dictionaries
        return pd.DataFrame(data)

    # 1. Query by title
    def query_by_title(self, search_string: str, exact_match: bool = False):
        if exact_match:
            # Exact title match
            return self.to_dataframe(self.session.query(Movie).filter(Movie.movie_name == search_string).all())
        else:
            # Wildcard match (case insensitive search)
            search_pattern = f"%{search_string}%"
            return self.to_dataframe(self.session.query(Movie).filter(Movie.movie_name.ilike(search_pattern)).all())
            

    # 2. Query by genre
    def query_by_genre(self, genre_name: str)-> pd.DataFrame:
        # Join with Genre table through MovieGenre
        return self.to_dataframe((
            self.session.query(Movie)
            .join(MovieGenre)
            .join(Genre)
            .filter(Genre.genre_name == genre_name)
            .all()
        ))

    # 3. Query by release date
    def query_by_release_date(self, start_date=None, end_date=None):
        query = self.session.query(Movie)
        if start_date:
            query = query.filter(Movie.movie_release_date >= start_date)
        if end_date:
            query = query.filter(Movie.movie_release_date <= end_date)
        return query.all()

    # 4. Query by keyword
    def query_by_keyword(self, keyword_name: str) -> pd.DataFrame:
        # Join with Keyword table through MovieKeyword
        return self.to_dataframe((
            self.session.query(Movie)
            .join(MovieKeyword)
            .join(Keyword)
            .filter(Keyword.keyword_name == keyword_name)
            .all()
        ))

    # 5. Query by person (actor, director, etc.)
    def query_by_person(self, person_name: str)  -> pd.DataFrame:
        # Join with Person table through MovieCredit
        return self.to_dataframe((
            self.session.query(Movie)
            .join(MovieCredit)
            .join(Person)
            .filter(Person.name == person_name)
            .all()
        ))

    # 6. Query by studio
    def query_by_studio(self, studio_name: str) -> pd.DataFrame:
        # Join with Studio table through MovieStudio
        return self.to_dataframe((
            self.session.query(Movie)
            .join(MovieStudio)
            .join(Studio)
            .filter(Studio.studio_name == studio_name)
            .all()
        ))
        
        
    def get_movie_details(self,result_df: pd.DataFrame) -> pd.DataFrame:
        # Convert the movie_id column of result_df to a list
        movie_ids = result_df['movie_id'].tolist()

        # Query MovieDetails for all movies with movie_id in movie_ids
        movies = self.session.query(MovieDetails).filter(MovieDetails.movie_id.in_(movie_ids)).all()

        # Convert the result to a pandas DataFrame
        movies_df = pd.DataFrame([movie.__dict__ for movie in movies])

        # Remove the SQLAlchemy internal attributes (like _sa_instance_state) if needed
        movies_df = movies_df.drop(columns=['_sa_instance_state'], errors='ignore')
        
        return movies_df
