"""
models.py

This module defines the database schema for a movie recommendation system using SQLAlchemy ORM. 
The database contains tables to store information about users, movies, genres, studios, keywords, 
and their relationships. Each table is represented as a class with attributes mapped to the columns 
in the database.

Classes:
--------
1. **Person**:
    Represents an individual (e.g., an actor or director) associated with a movie.

2. **User**:
    Represents a user in the system, storing login details, birthdate, and email.

3. **Mylist**:
    Represents the user's custom list of movies.

4. **WatchHistory**:
    Stores information about the user's watch history, including movie ratings and favorites.

5. **Genre**:
    Stores information about movie genres.

6. **Keyword**:
    Stores information about keywords associated with a movie (e.g., "thriller", "comedy").

7. **Studio**:
    Represents a movie studio that produced the movie.

8. **Movie**:
    Represents the main movie entity in the database, storing information such as name, release date, 
    summary, and related information such as credits, genres, studios, and keywords.

9. **MovieCredit**:
    Defines the many-to-many relationship between a movie and the people (e.g., actors or directors) 
    involved in making the movie.

10. **MovieKeyword**:
    Defines the many-to-many relationship between a movie and its keywords.

11. **MovieStudio**:
    Defines the many-to-many relationship between a movie and its associated studios.

12. **MovieGenre**:
    Defines the many-to-many relationship between a movie and its genres.

13. **MovieDetails**:
    A view that aggregates the full details of a movie, combining information about its name, 
    release date, summary, credits, genres, studios, and keywords.

Dependencies:
-------------
- SQLAlchemy ORM
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base

# Base class for all models
Base = declarative_base()


class Person(Base):
    """
    Represents an individual involved in a movie (e.g., actor, director).

    Attributes:
        person_id (int): Unique identifier for the person.
        name (str): Name of the person.
        person_birthdate (Date): Birthdate of the person.
        home_country (str): Country of origin for the person.
        credits (relationship): Relationship to the MovieCredit table.
    """
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    person_birthdate = Column(Date, nullable=True)
    home_country = Column(String, nullable=True)

    # Relationship with MovieCredit
    credits = relationship('MovieCredit', back_populates='person')


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        user_id (int): Unique identifier for the user.
        user_name (str): Username for login.
        user_birthdate (Date): Birthdate of the user.
        password (str): Password for the user.
        e_mail (str): Email address of the user.
        mylist (relationship): Relationship to the Mylist table.
        watch_history (relationship): Relationship to the WatchHistory table.
    """
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False, unique=True)
    user_birthdate = Column(Date, nullable=False)
    password = Column(String, nullable=False)
    e_mail = Column(String, nullable=False, unique=True)

    # Relationships with Mylist and WatchHistory
    mylist = relationship('Mylist', back_populates='user')
    watch_history = relationship('WatchHistory', back_populates='user')


class Mylist(Base):
    """
    Represents the movies added to a user's custom list.

    Attributes:
        user_id (int): Foreign key to the User table.
        movie_id (int): Foreign key to the Movie table.
        user (relationship): Relationship to the User table.
        movie (relationship): Relationship to the Movie table.
    """
    __tablename__ = 'mylist'
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)

    # Relationships
    user = relationship('User', back_populates='mylist')
    movie = relationship('Movie', back_populates='mylist')


class WatchHistory(Base):
    """
    Stores the user's watch history, including ratings and favorite status.

    Attributes:
        user_id (int): Foreign key to the User table.
        movie_id (int): Foreign key to the Movie table.
        watch_date (Date): The date when the movie was watched.
        rating (float): User's rating of the movie (optional).
        is_favorite (bool): Indicates whether the movie is a favorite.
        user (relationship): Relationship to the User table.
        movie (relationship): Relationship to the Movie table.
    """
    __tablename__ = 'watch_history'
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
    watch_date = Column(Date, nullable=False)
    rating = Column(Float, nullable=True)
    is_favorite = Column(Boolean, nullable=False)

    # Relationships
    user = relationship('User', back_populates='watch_history')
    movie = relationship('Movie', back_populates='watch_history')


class Genre(Base):
    """
    Represents a movie genre.

    Attributes:
        genre_id (int): Unique identifier for the genre.
        genre_name (str): Name of the genre.
        genres (relationship): Relationship to the MovieGenre table.
    """
    __tablename__ = 'genre'
    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    genre_name = Column(String, nullable=False, unique=True)

    genres = relationship('MovieGenre', back_populates='genre')


class Keyword(Base):
    """
    Represents a keyword associated with a movie.

    Attributes:
        keyword_id (int): Unique identifier for the keyword.
        keyword_name (str): Name of the keyword.
        keywords (relationship): Relationship to the MovieKeyword table.
    """
    __tablename__ = 'keyword'
    keyword_id = Column(Integer, primary_key=True, autoincrement=True)
    keyword_name = Column(String, nullable=False, unique=True)

    keywords = relationship('MovieKeyword', back_populates='keyword')


class Studio(Base):
    """
    Represents a movie studio.

    Attributes:
        studio_id (int): Unique identifier for the studio.
        studio_name (str): Name of the studio.
        studios (relationship): Relationship to the MovieStudio table.
    """
    __tablename__ = 'studio'
    studio_id = Column(Integer, primary_key=True, autoincrement=True)
    studio_name = Column(String, nullable=False, unique=True)

    studios = relationship('MovieStudio', back_populates='studio')


class Movie(Base):
    """
    Represents a movie.

    Attributes:
        movie_id (int): Unique identifier for the movie.
        movie_name (str): Name of the movie.
        movie_release_date (Date): Release date of the movie.
        movie_summary (str): Summary or description of the movie.
        mylist (relationship): Relationship to the Mylist table.
        watch_history (relationship): Relationship to the WatchHistory table.
        credits (relationship): Relationship to the MovieCredit table.
        keywords (relationship): Relationship to the MovieKeyword table.
        studios (relationship): Relationship to the MovieStudio table.
        genres (relationship): Relationship to the MovieGenre table.
    """
    __tablename__ = 'movie'
    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String, nullable=False)
    movie_release_date = Column(Date, nullable=True)
    movie_summary = Column(String, nullable=True)

    # Relationships
    mylist = relationship('Mylist', back_populates='movie')
    watch_history = relationship('WatchHistory', back_populates='movie')
    credits = relationship('MovieCredit', back_populates='movie')
    keywords = relationship('MovieKeyword', back_populates='movie')
    studios = relationship('MovieStudio', back_populates='movie')
    genres = relationship('MovieGenre', back_populates='movie')


class MovieCredit(Base):
    """
    Represents the relationship between a movie and a person involved in its production (e.g., actor, director).

    Attributes:
        movie_id (int): Foreign key to the Movie table.
        person_id (int): Foreign key to the Person table.
        movie (relationship): Relationship to the Movie table.
        person (relationship): Relationship to the Person table.
    """
    __tablename__ = 'movie_credit'
    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
    person_id = Column(Integer, ForeignKey('person.person_id'), primary_key=True)

    # Relationships
    movie = relationship('Movie', back_populates='credits')
    person = relationship('Person', back_populates='credits')


class MovieKeyword(Base):
    """
    Represents the relationship between a movie and a keyword.

    Attributes:
        movie_id (int): Foreign key to the Movie table.
        keyword_id (int): Foreign key to the Keyword table.
        movie (relationship): Relationship to the Movie table.
        keyword (relationship): Relationship to the Keyword table.
    """
    __tablename__ = 'movie_keyword'
    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keyword.keyword_id'), primary_key=True)

    # Relationships
    movie = relationship('Movie', back_populates='keywords')
    keyword = relationship('Keyword', back_populates='keywords')


class MovieStudio(Base):
    """
    Represents the relationship between a movie and a studio.

    Attributes:
        movie_id (int): Foreign key to the Movie table.
        studio_id (int): Foreign key to the Studio table.
        movie (relationship): Relationship to the Movie table.
        studio (relationship): Relationship to the Studio table.
    """
    __tablename__ = 'movie_studio'
    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
    studio_id = Column(Integer, ForeignKey('studio.studio_id'), primary_key=True)

    # Relationships
    movie = relationship('Movie', back_populates='studios')
    studio = relationship('Studio', back_populates='studios')


class MovieGenre(Base):
    """
    Represents the relationship between a movie and a genre.

    Attributes:
        movie_id (int): Foreign key to the Movie table.
        genre_id (int): Foreign key to the Genre table.
        movie (relationship): Relationship to the Movie table.
        genre (relationship): Relationship to the Genre table.
    """
    __tablename__ = 'movie_genre'
    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genre.genre_id'), primary_key=True)

    # Relationships
    movie = relationship('Movie', back_populates='genres')
    genre = relationship('Genre', back_populates='genres')


class MovieDetails(Base):
    """
    Represents a view that aggregates full details of a movie, including name, release date, 
    summary, credits, genres, studios, and keywords.

    Attributes:
        movie_id (int): Unique identifier for the movie.
        movie_name (str): Name of the movie.
        movie_release_date (Date): Release date of the movie.
        movie_summary (str): Summary or description of the movie.
        credits (str): Credits for the movie.
        genres (str): Genres associated with the movie.
        studios (str): Studios involved in the movie production.
        keywords (str): Keywords associated with the movie.
    """
    __tablename__ = 'movie_full_details'
    
    # Columns as represented in the view
    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String)
    movie_release_date = Column(Date)
    movie_summary = Column(String)
    credits = Column(String)
    genres = Column(String)
    studios = Column(String)
    keywords = Column(String)

    def __repr__(self):
        return (f"<MovieDetails(movie_id={self.movie_id}, movie_name={self.movie_name}, "
                f"movie_release_date={self.movie_release_date}, credits={self.credits}, "
                f"genres={self.genres}, studios={self.studios}, keywords={self.keywords})>")
