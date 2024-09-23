import pandas as pd
import sqlite3
from typing import Optional, List
from db.movie_app_db import WatchHistory
from app.services.base_types import Service


class WatchHistoryService(Service):
    """
    Service for managing user watch history in the movie application.
    
    This service provides CRUD operations for interacting with the watch history table in the database,
    such as creating, reading, updating, and deleting watch history entries.
    """

    def create_watch_history(
        self, user_id: int, movie_id: int, watch_date: Optional[str] = None,
        rating: Optional[float] = None, is_favorite: bool = False
    ):
        """
        Creates a new watch history record.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
            watch_date (Optional[str]): The date the movie was watched. Defaults to None.
            rating (Optional[float]): The rating given to the movie. Defaults to None.
            is_favorite (bool): Whether the movie is marked as a favorite. Defaults to False.
        """
        new_watch_history = WatchHistory(
            user_id=user_id, movie_id=movie_id, watch_date=watch_date, 
            rating=rating, is_favorite=is_favorite
        )
        self.session.add(new_watch_history)
        self.session.commit()

    def read_watch_history(self, user_id: int, movie_id: int) -> Optional[WatchHistory]:
        """
        Retrieves a specific watch history record by user ID and movie ID.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.

        Returns:
            Optional[WatchHistory]: The watch history record or None if not found.
        """
        return self.session.query(WatchHistory).filter_by(user_id=user_id, movie_id=movie_id).first()

    def read_user_watch_history(self, user_id: int) -> pd.DataFrame:
        """
        Retrieves all watch history records for a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            pd.DataFrame: DataFrame containing the user's watch history.
        """
        histories = self.session.query(WatchHistory).filter_by(user_id=user_id).all()
        return self.to_dataframe(histories)

    def read_all_watch_histories(self) -> pd.DataFrame:
        """
        Retrieves all watch history records for all users.

        Returns:
            pd.DataFrame: DataFrame containing all watch history records.
        """
        histories = self.session.query(WatchHistory).all()
        return self.to_dataframe(histories)

    def update_watch_history(
        self, user_id: int, movie_id: int, watch_date: Optional[str] = None,
        rating: Optional[float] = None, is_favorite: Optional[bool] = None
    ):
        """
        Updates an existing watch history record.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
            watch_date (Optional[str]): The updated watch date. Defaults to None.
            rating (Optional[float]): The updated rating. Defaults to None.
            is_favorite (Optional[bool]): Whether the movie is marked as a favorite. Defaults to None.
        """
        watch_history = self.read_watch_history(user_id, movie_id)
        if watch_history:
            if rating is not None:
                watch_history.rating = rating
            if is_favorite is not None:
                watch_history.is_favorite = is_favorite
            if watch_date is not None:
                watch_history.watch_date = watch_date
            self.session.commit()

    def delete_watch_history(self, user_id: int, movie_id: int):
        """
        Deletes a specific watch history record by user ID and movie ID.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
        """
        watch_history = self.read_watch_history(user_id, movie_id)
        if watch_history:
            self.session.delete(watch_history)
            self.session.commit()

    def delete_complete_watch_history(self, user_id: int):
        """
        Deletes all watch history records for a given user from the database.

        Args:
            user_id (int): The ID of the user.
        """
        conn = sqlite3.connect('movie_app.db')
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM watch_history WHERE user_id = ?", (user_id,))
            conn.commit()
            print(f"Deleted {cursor.rowcount} rows from watch_history.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            conn.close()

    def is_in_watchhistory(self, user_id: int, movie_ids: pd.Series) -> pd.Series:
        """
        Checks if a series of movie IDs is in the user's watch history.

        Args:
            user_id (int): The ID of the user.
            movie_ids (pd.Series): A series of movie IDs to check.

        Returns:
            pd.Series: A boolean series indicating whether each movie is in the user's watch history.
        """
        results = movie_ids.apply(lambda movie_id: self.read_watch_history(user_id, movie_id) is not None)
        return results.rename('in_watch_history')

