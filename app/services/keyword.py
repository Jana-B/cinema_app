from db.movie_app_db import Keyword
import pandas as pd
from typing import Optional

from app.services.base_types import Service


class KeywordService(Service):
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
    
    def get_id_by_name(self, keyword_name: str) -> int:
        """
        get keyword_id by name.

        Args:
            keyword_name (str): The name of the keyword to search for.

        Returns:
            keyword_id: as int
        """
        return self.session.query(Keyword).filter(Keyword.keyword_name == keyword_name).all()[0].keyword_id
