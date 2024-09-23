"""
movie_details.py

This module defines a function to display the details of a specific movie in a Streamlit web application. 
The function fetches movie details based on a given movie ID and displays them to the user.

Functions:
----------
1. **show_movie_details_page(movie_id: int, user_id: int)**:
    Displays the details of a movie including its name, release date, genres, studios, credits, keywords, 
    and summary.

Dependencies:
-------------
- Streamlit: Used for building the web application interface.
- Pandas: Used for handling data in DataFrame format.
- MovieService: A service that provides methods to fetch movie-related data.
"""

import streamlit as st
import pandas as pd
from app.services.movie import MovieService

def show_movie_details_page(movie_id: int, user_id: int):
    """
    Displays the details of a specified movie.

    Parameters:
        movie_id (int): The unique identifier of the movie whose details are to be displayed.
        user_id (int): The unique identifier of the user requesting the movie details.

    This function does the following:
    - Initializes the MovieService to interact with the movie database.
    - Checks if a valid movie_id is provided.
    - Fetches the movie details by converting the movie_id into a DataFrame.
    - Displays the movie's details if found; otherwise, it shows an error message.
    """
    
    # Instantiate the MovieService
    movie_service = MovieService()
    
    # Store user_id in session state
    st.session_state['user_id'] = user_id

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
