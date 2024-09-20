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

    
    def read_user_mylist(self, user_id: int) -> pd.DataFrame:
        """
        Retrieves all mylist records by user ID.

        Args:
            user_id (int): The ID of the user.        
        Returns:
            pd.DataFrame: dataframe with mylist result for user_id.
        """
        return self.to_dataframe(self.session.query(Mylist).filter_by(user_id=user_id))


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
                        
    
    def is_in_mylist(self, user_id: int, movie_ids: pd.Series) -> pd.Series:
        """
        Checks if a series of movies is in the user's MyList.

        Args:
            user_id (int): The ID of the user.
            movie_ids (pd.Series): The IDs of the movies.

        Returns:
            pd.Series: A boolean Series indicating whether each movie is in the user's MyList.
        """
        results = []

        # Iterate over each movie_id in the Series
        for movie_id in movie_ids:
            # Query the database to check if the movie is in the user's MyList
            movie_in_list = self.session.query(Mylist).filter_by(user_id=user_id, movie_id=movie_id).first() is not None
            
            # Append the result (boolean)
            results.append(movie_in_list)

        # Convert the results into a Pandas Series
        return pd.Series(results, index=movie_ids, name='in_mylist')

