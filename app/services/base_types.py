from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from typing import List
from pydantic import BaseModel

# Define the path to the SQLite database
database_path = 'sqlite:///movie_app.db'

class Service:
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