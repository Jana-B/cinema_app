from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_
from db.movie_app_db import (
    Movie, MovieGenre, Genre, MovieKeyword, Keyword,
    MovieCredit, Person, MovieStudio, Studio, MovieDetails, 
    User, WatchHistory, Mylist
)
import pandas as pd
from typing import List, Optional, Union
from pydantic import BaseModel

# Define the path to the SQLite database
database_path = 'sqlite:///movie_app.db'

class MovieService:
    """
    Service class to handle CRUD operations and queries related to movies, genres, keywords, persons, studios, users, watch histories, and user lists.
    """

    def __init__(self, session=None):
        """
        Initializes the MovieService and establishes a connection to the SQLite database.
        """
        if session:
            self.session = session
        else:
            engine = create_engine(database_path)
            Session = sessionmaker(bind=engine)
            self.session = Session()

    def to_dataframe(self, object_list: List[BaseModel]) -> pd.DataFrame:
        """
        Converts a list of SQLAlchemy model objects to a pandas DataFrame.

        Args:
            object_list (List[BaseModel]): List of SQLAlchemy model objects.

        Returns:
            pd.DataFrame: DataFrame containing the data from the objects.
        """
        data = [obj.__dict__ for obj in object_list]
        return pd.DataFrame(data)

    def query_by_title(self, search_string: str, exact_match: bool = False) -> pd.DataFrame:
        """
        Queries movies by title.

        Args:
            search_string (str): The title or partial title to search for.
            exact_match (bool): Whether to perform an exact match. Defaults to False.

        Returns:
            pd.DataFrame: DataFrame containing the query results.
        """
        if exact_match:
            return self.to_dataframe(self.session.query(Movie).filter(Movie.movie_name == search_string).all())
        else:
            search_pattern = f"%{search_string}%"
            return self.to_dataframe(self.session.query(Movie).filter(Movie.movie_name.ilike(search_pattern)).all())

    def query_by_genre(self, genre_name: str) -> pd.DataFrame:
        """
        Queries movies by genre.

        Args:
            genre_name (str): The name of the genre.

        Returns:
            pd.DataFrame: DataFrame containing the query results.
        """
        return self.to_dataframe((
            self.session.query(Movie)
            .join(MovieGenre)
            .join(Genre)
            .filter(Genre.genre_name == genre_name)
            .all()
        ))

    def query_by_release_date(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Movie]:
        """
        Queries movies by release date range.

        Args:
            start_date (Optional[str]): The start date for the query. Defaults to None.
            end_date (Optional[str]): The end date for the query. Defaults to None.

        Returns:
            List[Movie]: List of movies within the specified date range.
        """
        query = self.session.query(Movie)
        if start_date:
            query = query.filter(Movie.movie_release_date >= start_date)
        if end_date:
            query = query.filter(Movie.movie_release_date <= end_date)
        return query.all()

    def query_by_keyword(self, keyword_name: str) -> pd.DataFrame:
        """
        Queries movies by keyword.

        Args:
            keyword_name (str): The name of the keyword.

        Returns:
            pd.DataFrame: DataFrame containing the query results.
        """
        return self.to_dataframe((
            self.session.query(Movie)
            .join(MovieKeyword)
            .join(Keyword)
            .filter(Keyword.keyword_name == keyword_name)
            .all()
        ))

    def query_by_person(self, person_name: str) -> pd.DataFrame:
        """
        Queries movies by person (actor, director, etc.).

        Args:
            person_name (str): The name of the person.

        Returns:
            pd.DataFrame: DataFrame containing the query results.
        """
        return self.to_dataframe((
            self.session.query(Movie)
            .join(MovieCredit)
            .join(Person)
            .filter(Person.name == person_name)
            .all()
        ))

    def query_by_studio(self, studio_name: str) -> pd.DataFrame:
        """
        Queries movies by studio.

        Args:
            studio_name (str): The name of the studio.

        Returns:
            pd.DataFrame: DataFrame containing the query results.
        """
        return self.to_dataframe((
            self.session.query(Movie)
            .join(MovieStudio)
            .join(Studio)
            .filter(Studio.studio_name == studio_name)
            .all()
        ))

    def get_movie_details(self, result_df: pd.DataFrame) -> pd.DataFrame:
        """
        Retrieves detailed information for movies from a DataFrame of movie IDs.

        Args:
            result_df (pd.DataFrame): DataFrame containing movie IDs.

        Returns:
            pd.DataFrame: DataFrame containing detailed information for the movies.
        """
        movie_ids = result_df['movie_id'].tolist()
        movies = self.session.query(MovieDetails).filter(MovieDetails.movie_id.in_(movie_ids)).all()
        movies_df = pd.DataFrame([movie.__dict__ for movie in movies])
        movies_df = movies_df.drop(columns=['_sa_instance_state'], errors='ignore')
        return movies_df

    # -------- CRUD Operations for Person --------
    def create_person(self, name: str, birthdate: Optional[str] = None, home_country: Optional[str] = None):
        """
        Creates a new person record.

        Args:
            name (str): The name of the person.
            birthdate (Optional[str]): The birthdate of the person. Defaults to None.
            home_country (Optional[str]): The home country of the person. Defaults to None.
        """
        new_person = Person(name=name, person_birthdate=birthdate, home_country=home_country)
        self.session.add(new_person)
        self.session.commit()

    def read_person(self, person_id: int) -> Optional[Person]:
        """
        Retrieves a person record by ID.

        Args:
            person_id (int): The ID of the person.

        Returns:
            Optional[Person]: The Person object with the specified ID, or None if not found.
        """        
        return self.session.get(Person, person_id)


    def read_all_persons(self) -> pd.DataFrame:
        """
        Retrieves all person records.

        Returns:
            pd.DataFrame: DataFrame containing all person records.
        """
        persons = self.session.query(Person).all()
        return self.to_dataframe(persons)

    def update_person(self, person_id: int, name: Optional[str] = None, birthdate: Optional[str] = None, home_country: Optional[str] = None):
        """
        Updates an existing person record.

        Args:
            person_id (int): The ID of the person to update.
            name (Optional[str]): The new name of the person. Defaults to None.
            birthdate (Optional[str]): The new birthdate of the person. Defaults to None.
            home_country (Optional[str]): The new home country of the person. Defaults to None.
        """
        person = self.read_person(person_id)
        if person:
            if name:
                person.name = name
            if birthdate:
                person.person_birthdate = birthdate
            if home_country:
                person.home_country = home_country
            self.session.commit()

    def delete_person(self, person_id: int):
        """
        Deletes a person record by ID.

        Args:
            person_id (int): The ID of the person to delete.
        """
        person = self.read_person(person_id)
        if person:
            self.session.delete(person)
            self.session.commit()

    # -------- CRUD Operations for User --------
    def create_user(self, user_name: str, birthdate: str, password: str, e_mail: str):
        """
        Creates a new user record.

        Args:
            user_name (str): The name of the user.
            birthdate (str): The birthdate of the user.
            password (str): The password of the user.
            e_mail (str): The email of the user.
        """
        new_user = User(user_name=user_name, user_birthdate=birthdate, password=password, e_mail=e_mail)
        self.session.add(new_user)
        self.session.commit()

    def read_user(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user record by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Optional[User]: The User object with the specified ID, or None if not found.
        """        
        return self.session.get(User, user_id)


    def read_all_users(self) -> pd.DataFrame:
        """
        Retrieves all user records.

        Returns:
            pd.DataFrame: DataFrame containing all user records.
        """
        users = self.session.query(User).all()
        return self.to_dataframe(users)

    def update_user(self, user_id: int, user_name: Optional[str] = None, birthdate: Optional[str] = None, password: Optional[str] = None, e_mail: Optional[str] = None):
        """
        Updates an existing user record.

        Args:
            user_id (int): The ID of the user to update.
            user_name (Optional[str]): The new name of the user. Defaults to None.
            birthdate (Optional[str]): The new birthdate of the user. Defaults to None.
            password (Optional[str]): The new password of the user. Defaults to None.
            e_mail (Optional[str]): The new email of the user. Defaults to None.
        """
        user = self.read_user(user_id)
        if user:
            if user_name:
                user.user_name = user_name
            if birthdate:
                user.user_birthdate = birthdate
            if password:
                user.password = password
            if e_mail:
                user.e_mail = e_mail
            self.session.commit()

    def delete_user(self, user_id: int):
        """
        Deletes a user record by ID.

        Args:
            user_id (int): The ID of the user to delete.
        """
        user = self.read_user(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()

    # -------- CRUD Operations for Mylist --------
    def create_mylist(self, user_id: int, movie_id: int):
        """
        Creates a new mylist record.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
        """
        new_mylist = Mylist(user_id=user_id, movie_id=movie_id)
        self.session.add(new_mylist)
        self.session.commit()

    def read_mylist(self, user_id: int, movie_id: int) -> Optional[Mylist]:
        """
        Retrieves a mylist record by user ID and movie ID.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.

        Returns:
            Optional[Mylist]: The Mylist object with the specified IDs, or None if not found.
        """
        return self.session.query(Mylist).filter_by(user_id=user_id, movie_id=movie_id).first()

    def read_all_mylists(self) -> pd.DataFrame:
        """
        Retrieves all mylist records.

        Returns:
            pd.DataFrame: DataFrame containing all mylist records.
        """
        mylists = self.session.query(Mylist).all()
        return self.to_dataframe(mylists)

    def delete_mylist(self, user_id: int, movie_id: int):
        """
        Deletes a mylist record by user ID and movie ID.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
        """
        mylist = self.read_mylist(user_id, movie_id)
        if mylist:
            self.session.delete(mylist)
            self.session.commit()

    # -------- CRUD Operations for WatchHistory --------
    def create_watch_history(self, user_id: int, movie_id: int, watch_date: str, rating: Optional[float] = None, is_favorite: bool = False):
        """
        Creates a new watch history record.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
            watch_date (str): The date the movie was watched.
            rating (Optional[float]): The rating given to the movie. Defaults to None.
            is_favorite (bool): Whether the movie is marked as a favorite. Defaults to False.
        """
        new_watch_history = WatchHistory(user_id=user_id, movie_id=movie_id, watch_date=watch_date, rating=rating, is_favorite=is_favorite)
        self.session.add(new_watch_history)
        self.session.commit()

    def read_watch_history(self, user_id: int, movie_id: int) -> Optional[WatchHistory]:
        """
        Retrieves a watch history record by user ID and movie ID.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.

        Returns:
            Optional[WatchHistory]: The WatchHistory object with the specified IDs, or None if not found.
        """
        return self.session.query(WatchHistory).filter_by(user_id=user_id, movie_id=movie_id).first()

    def read_all_watch_histories(self) -> pd.DataFrame:
        """
        Retrieves all watch history records.

        Returns:
            pd.DataFrame: DataFrame containing all watch history records.
        """
        histories = self.session.query(WatchHistory).all()
        return self.to_dataframe(histories)

    def update_watch_history(self, user_id: int, movie_id: int, rating: Optional[float] = None, is_favorite: Optional[bool] = None):
        """
        Updates an existing watch history record.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
            rating (Optional[float]): The new rating of the movie. Defaults to None.
            is_favorite (Optional[bool]): Whether the movie is marked as a favorite. Defaults to None.
        """
        watch_history = self.read_watch_history(user_id, movie_id)
        if watch_history:
            if rating is not None:
                watch_history.rating = rating
            if is_favorite is not None:
                watch_history.is_favorite = is_favorite
            self.session.commit()

    def delete_watch_history(self, user_id: int, movie_id: int):
        """
        Deletes a watch history record by user ID and movie ID.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
        """
        watch_history = self.read_watch_history(user_id, movie_id)
        if watch_history:
            self.session.delete(watch_history)
            self.session.commit()

    # -------- CRUD Operations for Genre --------
    def create_genre(self, genre_name: str):
        """
        Creates a new genre record.

        Args:
            genre_name (str): The name of the genre.
        """
        new_genre = Genre(genre_name=genre_name)
        self.session.add(new_genre)
        self.session.commit()

    def read_genre(self, genre_id: int) -> Optional[Genre]:
        """
        Retrieves a genre record by ID.

        Args:
            genre_id (int): The ID of the genre.

        Returns:
            Optional[Genre]: The Genre object with the specified ID, or None if not found.
        """    
        return self.session.get(Genre, genre_id)


    def read_all_genres(self) -> pd.DataFrame:
        """
        Retrieves all genre records.

        Returns:
            pd.DataFrame: DataFrame containing all genre records.
        """
        genres = self.session.query(Genre).all()
        return self.to_dataframe(genres)

    def update_genre(self, genre_id: int, genre_name: str):
        """
        Updates an existing genre record.

        Args:
            genre_id (int): The ID of the genre to update.
            genre_name (str): The new name of the genre.
        """
        genre = self.read_genre(genre_id)
        if genre:
            genre.genre_name = genre_name
            self.session.commit()

    def delete_genre(self, genre_id: int):
        """
        Deletes a genre record by ID.

        Args:
            genre_id (int): The ID of the genre to delete.
        """
        genre = self.read_genre(genre_id)
        if genre:
            self.session.delete(genre)
            self.session.commit()

    # -------- CRUD Operations for Keyword --------
    def create_keyword(self, keyword_name: str):
        """
        Creates a new keyword record.

        Args:
            keyword_name (str): The name of the keyword.
        """
        new_keyword = Keyword(keyword_name=keyword_name)
        self.session.add(new_keyword)
        self.session.commit()

    def read_keyword(self, keyword_id: int) -> Optional[Keyword]:
        """
        Retrieves a keyword record by ID.

        Args:
            keyword_id (int): The ID of the keyword.

        Returns:
            Optional[Keyword]: The Keyword object with the specified ID, or None if not found.
        """        
        return self.session.get(Keyword, keyword_id)


    def read_all_keywords(self) -> pd.DataFrame:
        """
        Retrieves all keyword records.

        Returns:
            pd.DataFrame: DataFrame containing all keyword records.
        """
        keywords = self.session.query(Keyword).all()
        return self.to_dataframe(keywords)

    def update_keyword(self, keyword_id: int, keyword_name: str):
        """
        Updates an existing keyword record.

        Args:
            keyword_id (int): The ID of the keyword to update.
            keyword_name (str): The new name of the keyword.
        """
        keyword = self.read_keyword(keyword_id)
        if keyword:
            keyword.keyword_name = keyword_name
            self.session.commit()

    def delete_keyword(self, keyword_id: int):
        """
        Deletes a keyword record by ID.

        Args:
            keyword_id (int): The ID of the keyword to delete.
        """
        keyword = self.read_keyword(keyword_id)
        if keyword:
            self.session.delete(keyword)
            self.session.commit()

    # -------- CRUD Operations for Studio --------
    def create_studio(self, studio_name: str):
        """
        Creates a new studio record.

        Args:
            studio_name (str): The name of the studio.
        """
        new_studio = Studio(studio_name=studio_name)
        self.session.add(new_studio)
        self.session.commit()

    def read_studio(self, studio_id: int) -> Optional[Studio]:
        """
        Retrieves a studio record by ID.

        Args:
            studio_id (int): The ID of the studio.

        Returns:
            Optional[Studio]: The Studio object with the specified ID, or None if not found.
        """
        return self.session.get(Studio, studio_id)


    def read_all_studios(self) -> pd.DataFrame:
        """
        Retrieves all studio records.

        Returns:
            pd.DataFrame: DataFrame containing all studio records.
        """
        studios = self.session.query(Studio).all()
        return self.to_dataframe(studios)

    def update_studio(self, studio_id: int, studio_name: str):
        """
        Updates an existing studio record.

        Args:
            studio_id (int): The ID of the studio to update.
            studio_name (str): The new name of the studio.
        """
        studio = self.read_studio(studio_id)
        if studio:
            studio.studio_name = studio_name
            self.session.commit()

    def delete_studio(self, studio_id: int):
        """
        Deletes a studio record by ID.

        Args:
            studio_id (int): The ID of the studio to delete.
        """
        studio = self.read_studio(studio_id)
        if studio:
            self.session.delete(studio)
            self.session.commit()

    # -------- CRUD Operations for Movie and Associations --------
    def create_movie(self, movie_name: str, release_date: Optional[str] = None, summary: Optional[str] = None):
        """
        Creates a new movie record.

        Args:
            movie_name (str): The name of the movie.
            release_date (Optional[str]): The release date of the movie. Defaults to None.
            summary (Optional[str]): The summary of the movie. Defaults to None.
        """
        new_movie = Movie(movie_name=movie_name, movie_release_date=release_date, movie_summary=summary)
        self.session.add(new_movie)
        self.session.commit()

    def read_movie(self, movie_id: int) -> Optional[Movie]:
        """
        Retrieves a movie record by ID.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            Optional[Movie]: The Movie object with the specified ID, or None if not found.
        """        
        return self.session.get(Movie, movie_id)


    def read_all_movies(self) -> pd.DataFrame:
        """
        Retrieves all movie records.

        Returns:
            pd.DataFrame: DataFrame containing all movie records.
        """
        movies = self.session.query(Movie).all()
        return self.to_dataframe(movies)

    def update_movie(self, movie_id: int, movie_name: Optional[str] = None, release_date: Optional[str] = None, summary: Optional[str] = None):
        """
        Updates an existing movie record.

        Args:
            movie_id (int): The ID of the movie to update.
            movie_name (Optional[str]): The new name of the movie. Defaults to None.
            release_date (Optional[str]): The new release date of the movie. Defaults to None.
            summary (Optional[str]): The new summary of the movie. Defaults to None.
        """
        movie = self.read_movie(movie_id)
        if movie:
            if movie_name:
                movie.movie_name = movie_name
            if release_date:
                movie.movie_release_date = release_date
            if summary:
                movie.movie_summary = summary
            self.session.commit()

    def delete_movie(self, movie_id: int):
        """
        Deletes a movie record by ID.

        Args:
            movie_id (int): The ID of the movie to delete.
        """
        movie = self.read_movie(movie_id)
        if movie:
            self.session.delete(movie)
            self.session.commit()

    # -------- Distinct Value Retrieval Methods --------
    def get_distinct_genre_names(self) -> list[str]:
        """
        Retrieves a list of distinct genre names.

        Returns:
            list[str]: A list of distinct genre names.
        """
        return [g.genre_name for g in self.session.query(Genre.genre_name).distinct()]

    def get_distinct_keyword_names(self) -> list[str]:
        """
        Retrieves a list of distinct keyword names.

        Returns:
            list[str]: A list of distinct keyword names.
        """
        return [k.keyword_name for k in self.session.query(Keyword.keyword_name).distinct()]

    def get_distinct_person_names(self) -> list[str]:
        """
        Retrieves a list of distinct person names.

        Returns:
            list[str]: A list of distinct person names.
        """
        return [p.name for p in self.session.query(Person.name).distinct()]

    def get_distinct_studio_names(self) -> list[str]:
        """
        Retrieves a list of distinct studio names.

        Returns:
            list[str]: A list of distinct studio names.
        """
        return [s.studio_name for s in self.session.query(Studio.studio_name).distinct()]
