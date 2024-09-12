from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from db.movie_app_db import Movie, Genre, Keyword, Studio, Person, MovieGenre, MovieKeyword, MovieCredit, MovieStudio
                            

# Connect to the SQLite database
engine = create_engine('sqlite:///movie_app.db')
Session = sessionmaker(bind=engine)
session = Session()

# Load the CSV file
movie_data = pd.read_csv('data/movies.csv')

# Helper function to add unique items and return their objects
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

# Process and import data from the CSV
for index, row in movie_data.iterrows():
    # Create or get Movie object
    movie = Movie(
        movie_id=row['id'],
        movie_name=row['title'],
        movie_release_date=pd.to_datetime(row['release_date']),
        movie_summary=row['overview']
    )   
    
    session.add(movie)
    
    # Process and add genres
    if pd.notna(row['genres']):
        genres = row['genres'].split('-')
        for genre_name in genres:
            genre = get_or_create(session, Genre, genre_name=genre_name.strip())
            get_or_create(session, MovieGenre, 
                          movie_id = movie.movie_id,
                          genre_id = genre.genre_id)                        
            
    # Process and add keywords
    if pd.notna(row['keywords']):
        keywords = row['keywords'].split('-')
        for keyword_name in keywords:
            keyword = get_or_create(session, Keyword, keyword_name=keyword_name.strip())
            get_or_create(session, MovieKeyword, 
                          movie_id = movie.movie_id,
                          keyword_id = keyword.keyword_id)
    
    # Process and add studios (production companies)
    if pd.notna(row['production_companies']):
        studios = row['production_companies'].split('-')
        for studio_name in studios:
            studio = get_or_create(session, Studio, studio_name=studio_name.strip())
            get_or_create(session, MovieStudio, 
                          movie_id = movie.movie_id,
                          studio_id = studio.studio_id)
                
    # Process and add credits
    if pd.notna(row['credits']):
        movie_credits = row['credits'].split('-')
        for person_name in movie_credits:
            person = get_or_create(session, Person, name=person_name.strip())                        
            get_or_create(session, MovieCredit, 
                          movie_id = movie.movie_id,
                          person_id = person.person_id)
                        

    

    # Commit the movie and relationships
    session.commit()

print("Data import complete!")

# Close the session
session.close()
