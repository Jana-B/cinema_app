from db.movie_app_db import Studio
import pandas as pd
from typing import Optional

from app.services.base_types import Service


class StudioService(Service):
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
    
    def get_id_by_name(self, studio_name: str) -> int:
        """
        get studio_id by name.

        Args:
            studio_name (str): The name of the studio to search for.

        Returns:
            studio_id: as int
        """
        return self.session.query(Studio).filter(Studio.studio_name == studio_name).all()[0].studio_id