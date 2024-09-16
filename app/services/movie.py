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

from app.services.base_types import Service


class MovieService(Service):
    """
    Service class to handle CRUD operations and queries related to movies, genres, keywords, persons, studios, users, watch histories, and user lists.
    """

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
