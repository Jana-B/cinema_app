from db.movie_app_db import WatchHistory
import pandas as pd
from typing import Optional

from app.services.base_types import Service



class WatchHistoryService(Service):
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
    
    def is_in_watchhistory(self, user_id: int, movie_ids: pd.Series) -> pd.Series:
        """
        Checks if a series of movies is in the user's WatchHistory.

        Args:
            user_id (int): The ID of the user.
            movie_ids (pd.Series): The IDs of the movies.

        Returns:
            pd.Series: A boolean Series indicating whether each movie is in the user's watch history.
        """
        results = []

        # Iterate over each movie_id in the Series
        for movie_id in movie_ids:
            # Query the database to check if the movie is in the user's watch history
            movie_in_watchhistory = self.session.query(WatchHistory).filter_by(user_id=user_id, movie_id=movie_id).first() is not None
            
            # Append the result (boolean)
            results.append(movie_in_watchhistory)

        # Convert the results into a Pandas Series
        return pd.Series(results, index=movie_ids, name='in_watch_history')
