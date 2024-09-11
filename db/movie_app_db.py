from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    person_birthdate = Column(Date, nullable=True)
    home_country = Column(String, nullable=True)

    # Relationship with MovieCredit
    credits = relationship('MovieCredit', back_populates='person')
            
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
    genre_name = Column(String, nullable=False, unique=True) 
    
    genres = relationship('MovieGenre', back_populates='genre')

class Keyword(Base):
    __tablename__ = 'keyword'
    keyword_id = Column(Integer, primary_key=True)
    keyword_name = Column(String, nullable=False, unique=True)
    
    keywords = relationship('MovieKeyword', back_populates='keyword')

class Studio(Base):
    __tablename__ = 'studio'
    studio_id = Column(Integer, primary_key=True)
    studio_name = Column(String, nullable=False, unique=True)
    
    studios = relationship('MovieStudio', back_populates='studio')

class Movie(Base):
    __tablename__ = 'movie'
    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String, nullable=False, unique=False)
    movie_release_date = Column(Date, nullable=True)
    movie_summary = Column(String, nullable=True)

    # Relationships with Mylist, WatchHistory
    mylist = relationship('Mylist', back_populates='movie')
    watch_history = relationship('WatchHistory', back_populates='movie')

    # Relationship with MovieCredit, MovieKeyword, MovieStudio, MovieGenre
    credits = relationship('MovieCredit', back_populates='movie')
    keywords = relationship('MovieKeyword', back_populates='movie')
    studios = relationship('MovieStudio', back_populates='movie')
    genres = relationship('MovieGenre', back_populates='movie')

class MovieCredit(Base):
    __tablename__ = 'movie_credit'
    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
    person_id = Column(Integer, ForeignKey('person.person_id'), primary_key=True)

    # Relationships
    movie = relationship('Movie', back_populates='credits')  # Correct relationship name 'credits'
    person = relationship('Person', back_populates='credits')  # Correct back_populates to 'credits'

class MovieKeyword(Base):
    __tablename__ = 'movie_keyword'
    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keyword.keyword_id'), primary_key=True)

    # Relationships
    movie = relationship('Movie', back_populates='keywords')
    keyword = relationship('Keyword', back_populates='keywords')

class MovieStudio(Base):
    __tablename__ = 'movie_studio'
    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
    studio_id = Column(Integer, ForeignKey('studio.studio_id'), primary_key=True)

    # Relationships
    movie = relationship('Movie', back_populates='studios')
    studio = relationship('Studio', back_populates='studios')
    
class MovieGenre(Base):
    __tablename__ = 'movie_genre'
    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genre.genre_id'), primary_key=True)

    # Relationships
    movie = relationship('Movie', back_populates='genres')
    genre = relationship('Genre', back_populates='genres')

class MovieDetails(Base):
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
