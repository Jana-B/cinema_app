from sqlalchemy import create_engine, text
import pandas as pd

# Connect to the SQLite database
engine = create_engine('sqlite:///movie_app.db')

# Load the CSV file
movie_data = pd.read_csv('data/movies.csv')

# Step 1: Insert Persons, Genres, Keywords, Studios in bulk
def insert_foreign_key_data(connection, column, table, data):
    """
    Insert unique entries into the foreign key table (e.g., persons, genres, keywords, studios).
    """
    unique_data = set(item.strip() for items in data if pd.notna(items) for item in items.split('-'))
    
    sql = f"""
    INSERT INTO {table} ({column})
    VALUES (:value)
    ON CONFLICT ({column}) DO NOTHING
    """
    
    connection.execute(text(sql), [{'value': item} for item in unique_data])
    connection.execute(text('COMMIT'))

def build_insert_statements():
    with engine.connect() as connection:
        # Insert Genres
        insert_foreign_key_data(connection, 'genre_name', 'genre', movie_data['genres'])
        
        # Insert Keywords
        insert_foreign_key_data(connection, 'keyword_name', 'keyword', movie_data['keywords'])
        
        # Insert Studios
        insert_foreign_key_data(connection, 'studio_name', 'studio', movie_data['production_companies'])
        
        # Insert Persons (Credits)
        insert_foreign_key_data(connection, 'name', 'person', movie_data['credits'])

# Step 2: Helper function to get the ID from the database
def get_foreign_key_id(connection, table, column, value):
    """
    Retrieves the ID of a foreign key (e.g., genre_id, person_id, studio_id) based on the column value.
    """
    sql = text(f"SELECT {table}_id FROM {table} WHERE {column} = :value")
    result = connection.execute(sql, {'value': value}).fetchone()
    return result[0] if result else None

# Step 3: Insert Movies and their relationships
def insert_movies_and_relationships(connection, row):
    """
    Inserts the movie and its relationships (genres, keywords, studios, credits) into the database.
    """
    if pd.isna(row['title']):
        # Log or print movies without a title
        print(f"Skipped movie with ID {row['id']} due to missing title")
        return
    
    # Insert Movie
    movie_sql = text("""
    INSERT INTO movie (movie_id, movie_name, movie_release_date, movie_summary)
    VALUES (:movie_id, :movie_name, :movie_release_date, :movie_summary)
    ON CONFLICT (movie_id) DO NOTHING
    """)
    connection.execute(movie_sql, {
        'movie_id': row['id'],
        'movie_name': row['title'],
        'movie_release_date': row['release_date'],
        'movie_summary': row['overview']
    })
        
    # Insert Movie-Genre Relationship
    if pd.notna(row['genres']):
        genres = row['genres'].split('-')
        for genre in genres:
            genre_id = get_foreign_key_id(connection, 'genre', 'genre_name', genre.strip())
            if genre_id:
                genre_sql = text("""
                INSERT INTO movie_genre (movie_id, genre_id)
                VALUES (:movie_id, :genre_id)
                ON CONFLICT DO NOTHING
                """)
                connection.execute(genre_sql, {
                    'movie_id': row['id'],
                    'genre_id': genre_id
                })
    
    # Insert Movie-Keyword Relationship
    if pd.notna(row['keywords']):
        keywords = row['keywords'].split('-')
        for keyword in keywords:
            keyword_id = get_foreign_key_id(connection, 'keyword', 'keyword_name', keyword.strip())
            if keyword_id:
                keyword_sql = text("""
                INSERT INTO movie_keyword (movie_id, keyword_id)
                VALUES (:movie_id, :keyword_id)
                ON CONFLICT DO NOTHING
                """)
                connection.execute(keyword_sql, {
                    'movie_id': row['id'],
                    'keyword_id': keyword_id
                })
    
    # Insert Movie-Studio Relationship
    if pd.notna(row['production_companies']):
        studios = row['production_companies'].split('-')
        for studio in studios:
            studio_id = get_foreign_key_id(connection, 'studio', 'studio_name', studio.strip())
            if studio_id:
                studio_sql = text("""
                INSERT INTO movie_studio (movie_id, studio_id)
                VALUES (:movie_id, :studio_id)
                ON CONFLICT DO NOTHING
                """)
                connection.execute(studio_sql, {
                    'movie_id': row['id'],
                    'studio_id': studio_id
                })
    
    # Insert Movie-Credit Relationship
    if pd.notna(row['credits']):
        credits = row['credits'].split('-')
        for person in credits:
            person_id = get_foreign_key_id(connection, 'person', 'name', person.strip())
            if person_id:
                credit_sql = text("""
                INSERT INTO movie_credit (movie_id, person_id)
                VALUES (:movie_id, :person_id)
                ON CONFLICT DO NOTHING
                """)
                connection.execute(credit_sql, {
                    'movie_id': row['id'],
                    'person_id': person_id
                })

def insert_all_movies_and_relationships(batch_size=10000):
    """
    Insert movies and their relationships into the database with a commit after every `batch_size` movies.
    """
    with engine.connect() as connection:
        batch = []
        for _, row in movie_data.iterrows():
            batch.append(row)
            if len(batch) >= batch_size:
                # Process the batch
                for movie_row in batch:
                    insert_movies_and_relationships(connection, movie_row)
                # Commit the batch
                connection.execute(text('COMMIT'))
                print(f"Committed batch of {batch_size} movies")
                batch = []

        # Process any remaining movies in the last batch
        if batch:
            for movie_row in batch:
                insert_movies_and_relationships(connection, movie_row)
            connection.execute(text('COMMIT'))
            print(f"Committed remaining {len(batch)} movies")

# Execute the steps
build_insert_statements()  # Phase 1: Insert foreign key data
insert_all_movies_and_relationships()  # Phase 2: Insert movies and relationships

print("Data import complete using raw SQL!")
