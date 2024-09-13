from db.movie_app_db import Mylist
import pandas as pd
from typing import Optional


from app.services.base_types import Service


class MylistService(Service):
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
