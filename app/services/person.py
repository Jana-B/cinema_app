from db.movie_app_db import Person
import pandas as pd
from typing import Optional

from app.services.base_types import Service

class PersonService(Service):
    
    def create_person(self, name: str, birthdate: Optional[str] = None, home_country: Optional[str] = None):
        """
        Creates a new person record.

        Args:
            name (str): The name of the person.
            birthdate (Optional[str]): The birthdate of the person. Defaults to None.
            home_country (Optional[str]): The home country of the person. Defaults to None.
        """
        new_person = Person(name=name, person_birthdate=birthdate, home_country=home_country)
        self.session.add(new_person)
        self.session.commit()

    def read_person(self, person_id: int) -> Optional[Person]:
        """
        Retrieves a person record by ID.

        Args:
            person_id (int): The ID of the person.

        Returns:
            Optional[Person]: The Person object with the specified ID, or None if not found.
        """        
        return self.session.get(Person, person_id)


    def read_all_persons(self) -> pd.DataFrame:
        """
        Retrieves all person records.

        Returns:
            pd.DataFrame: DataFrame containing all person records.
        """
        persons = self.session.query(Person).all()
        return self.to_dataframe(persons)

    def update_person(self, person_id: int, name: Optional[str] = None, birthdate: Optional[str] = None, home_country: Optional[str] = None):
        """
        Updates an existing person record.

        Args:
            person_id (int): The ID of the person to update.
            name (Optional[str]): The new name of the person. Defaults to None.
            birthdate (Optional[str]): The new birthdate of the person. Defaults to None.
            home_country (Optional[str]): The new home country of the person. Defaults to None.
        """
        person = self.read_person(person_id)
        if person:
            if name:
                person.name = name
            if birthdate:
                person.person_birthdate = birthdate
            if home_country:
                person.home_country = home_country
            self.session.commit()

    def delete_person(self, person_id: int):
        """
        Deletes a person record by ID.

        Args:
            person_id (int): The ID of the person to delete.
        """
        person = self.read_person(person_id)
        if person:
            self.session.delete(person)
            self.session.commit()