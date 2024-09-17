import streamlit as st
import pandas as pd
from app.services.movie import MovieService

def show_movie_details_page(movie_id: int):
    # Instantiate the MovieService
    movie_service = MovieService()

    if 'user_id' in st.session_state:
        user_id = st.session_state['user_id']

    if movie_id:
        # Convert movie_id to a DataFrame (MovieService expects a DataFrame)
        movie_id_df = pd.DataFrame({"movie_id": [int(movie_id)]})

        # Fetch the movie details using MovieService
        movie_details = movie_service.get_movie_details(movie_id_df)

        # Check if movie details were found
        if not movie_details.empty:
            movie = movie_details.iloc[0]  # Extract the first row (single movie)

            # Display movie details
            st.title(movie["movie_name"])
            st.subheader(f"Release Date: {movie['movie_release_date'].strftime('%Y-%m-%d')}")
            st.write(f"Genres: {movie['genres']}")
            st.write(f"Studios: {movie['studios']}")
            st.write(f"Credits: {movie['credits']}")
            st.write(f"Keywords: {movie['keywords']}")
            st.write(f"Summary: {movie['movie_summary']}")
        else:
            st.write("No movie details found for the given movie ID.")
    else:
        st.write("No movie selected. Please select a movie from the search results.")
