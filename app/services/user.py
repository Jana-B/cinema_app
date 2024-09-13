from db.movie_app_db import User
import pandas as pd
from typing import Optional


from app.services.base_types import Service


class UserService(Service):
    
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