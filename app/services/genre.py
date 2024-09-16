from db.movie_app_db import Genre
import pandas as pd
from typing import Optional

from app.services.base_types import Service


class GenreService(Service):
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