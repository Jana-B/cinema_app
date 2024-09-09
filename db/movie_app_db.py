from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    person_birthdate = Column(Date, nullable=False)
    home_country = Column(String, nullable=False)

    # Relationship with MovieParticipation
    movie_participations = relationship('MovieParticipation', back_populates='person')

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    user_birthdate = Column(Date, nullable=False)
    password = Column(String, nullable=False)
    e_mail = Column(String, nullable=False)

    # Relationships with Mylist and WatchHistory
    mylist = relationship('Mylist', back_populates='user')
    watch_history = relationship('WatchHistory', back_populates='user')

class Mylist(Base):
    __tablename__ = 'mylist'
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)

    # Relationships
    user = relationship('User', back_populates='mylist')
    movie = relationship('Movie', back_populates='mylist')

class WatchHistory(Base):
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
    __tablename__ = 'genre'
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String, nullable=False)

    # One-to-many relationship with Movie
    movies = relationship('Movie', back_populates='genre')

class Studio(Base):
    __tablename__ = 'studio'
    studio_id = Column(Integer, primary_key=True)
    studio_name = Column(String, nullable=False)

    # One-to-many relationship with Movie
    movies = relationship('Movie', back_populates='studio')

class Movie(Base):
    __tablename__ = 'movie'
    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String, nullable=False)
    movie_release_date = Column(Date, nullable=False)
    movie_summary = Column(String, nullable=True)
    genre_id = Column(Integer, ForeignKey('genre.genre_id'), nullable=False)
    studio_id = Column(Integer, ForeignKey('studio.studio_id'), nullable=False)

    # Relationships with Genre, Studio, Mylist, WatchHistory
    genre = relationship('Genre', back_populates='movies')
    studio = relationship('Studio', back_populates='movies')
    mylist = relationship('Mylist', back_populates='movie')
    watch_history = relationship('WatchHistory', back_populates='movie')

    # Relationship with MovieParticipation
    participations = relationship('MovieParticipation', back_populates='movie')

class MovieParticipation(Base):
    __tablename__ = 'movie_participation'
    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
    person_id = Column(Integer, ForeignKey('person.person_id'), primary_key=True)

    # Relationships
    movie = relationship('Movie', back_populates='participations')
    person = relationship('Person', back_populates='movie_participations')
