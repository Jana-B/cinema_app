"""
movie_search.py

This module contains the logic for the movie search view of the movie recommendation app.

Overview:
---------
The movie search view allows users to search for movies based on various filters and 
display relevant search results. It interacts with the MovieService to retrieve 
movie data from the database and displays it in the Streamlit interface.

Features:
---------
1. **Search by Title**: 
- Users can input a movie title or partial title in the search field to find movies 
  that match the query.

2. **Filters**:
- **Genre**: Users can filter search results by selecting one or more genres from 
  a dropdown list.
- **Release Year**: Allows filtering of movies by release year or a range of years.
- **Rating**: Users can filter results based on minimum average ratings.

3. **Display of Results**:
- Displays the title, release year, genre(s), and rating of each movie found.
- If no movies match the search query, an appropriate message is shown to the user.
- Each result includes clickable links to the movie details page for 
  more in-depth information.

Usage:
------
This module is used in the main Streamlit app (`main.py`) as part of the movie recommendation 
system. The `show_movie_search_page()` function defines the layout and interactivity 
of the search view. It takes user input, queries the `MovieService` for matching movies, 
and renders the search results dynamically.

Dependencies:
-------------
- Streamlit for UI components and layout management.
- `MovieService` from the `services.movie_service` module for handling search and filtering 
  logic based on database queries.
"""

import streamlit as st
import pandas as pd
from app.services.movie import MovieService 
from app.services.mylist import MylistService 
from app.services.watchhistory import WatchHistoryService 
from datetime import datetime


def show_movie_search_page(user_id: int):
    """
    Displays the movie search page, allowing users to search for movies by various criteria 
    such as title, genres, studios, and keywords. Search results are displayed dynamically.

    Args:
        user_id (int): The ID of the user currently using the app.

    Returns:
        None
    """
    st.query_params.clear()
    st.query_params.page = "movie_search"

    movie_service = MovieService()
    st.title("Movie Search")

    # Filters
    st.sidebar.header("Filters")
    
    # Search bar
    search_query = st.sidebar.text_input("Search for a movie by title")

    # Genre Multi-select
    genres = movie_service.get_distinct_genre_names()
    selected_genres = st.sidebar.multiselect("Genres", genres)

    # Credits (People involved)
    selected_persons = st.sidebar.text_input("Persons")

    # Studio
    selected_studios = st.sidebar.text_input("Studios")

    # Keywords
    selected_keywords = st.sidebar.text_input("Keywords")

    # Search Button
    if st.sidebar.button("Search"):
        # Execute search queries based on user inputs
        result_sets = execute_queries(movie_service, search_query, selected_genres, selected_persons, selected_studios, selected_keywords)

        # Filter and display movies that match the search criteria
        if result_sets and not result_sets[0].empty:
            filtered_movies_df = intersect_results(result_sets)

            if not filtered_movies_df.empty:
                update_with_user_data(filtered_movies_df, user_id)
                display_search_result(filtered_movies_df)
                st.session_state['last_search_result'] = filtered_movies_df
            else:
                st.write("No movies found with the selected criteria.")
    elif 'last_search_result' in st.session_state:
        # Display previously searched results if available
        filtered_movies_df = st.session_state['last_search_result']
        update_with_user_data(filtered_movies_df, user_id)
        display_search_result(filtered_movies_df)


def execute_queries(movie_service, search_query: str, selected_genres: list, selected_persons: str, selected_studios: str, selected_keywords: str) -> list:
    """
    Executes a set of queries based on the user-provided search criteria.

    Args:
        movie_service (MovieService): An instance of MovieService to query movie data.
        search_query (str): A movie title or partial title to search for.
        selected_genres (list): List of genres to filter movies by.
        selected_persons (str): A string of persons (directors, actors, etc.) involved in the movie.
        selected_studios (str): A string of studios that produced the movie.
        selected_keywords (str): A string of keywords to filter movies by.

    Returns:
        list: A list of DataFrames, each containing results for a particular filter.
    """
    result_sets = []
    
    if search_query:
        movies_by_title = movie_service.query_by_title(search_query)
        result_sets.append(movies_by_title)

    if selected_genres:
        movies_by_genre = movie_service.query_by_genre(selected_genres)
        result_sets.append(movies_by_genre)

    if selected_keywords:
        movies_by_keyword = movie_service.query_by_keyword(selected_keywords)
        result_sets.append(movies_by_keyword)

    if selected_persons:
        movies_by_person = movie_service.query_by_person(selected_persons)
        result_sets.append(movies_by_person)

    if selected_studios:
        movies_by_studio = movie_service.query_by_studio(selected_studios)
        result_sets.append(movies_by_studio)

    return result_sets


def display_search_result(filtered_movies_df: pd.DataFrame):
    """
    Displays the search result movies in the Streamlit app, with options to add/remove them 
    to/from "Mylist" and "Watchhistory".

    Args:
        filtered_movies_df (pd.DataFrame): The DataFrame containing the filtered movies to display.

    Returns:
        None
    """
    mylist_service = MylistService()
    watch_history_service = WatchHistoryService()

    user_id = st.session_state.get('user_id', 0)

    for movie in filtered_movies_df.itertuples():
        movie_details_url = f"/?page=movie_details&movie_id={movie.movie_id}&user_id={user_id}"
        html_content = f"""
        <hr>
        <div style='margin-bottom: 20px;'>
            <h3><a href="{movie_details_url}" target="_self">{movie.movie_name}</a></h3>
            <p><strong>Release Date:</strong> {movie.movie_release_date}</p>
            <p><strong>Summary:</strong> {movie.movie_summary}</p>
        </div>        
        """
        st.markdown(html_content, unsafe_allow_html=True)

        if user_id != 0:
            # Handle checkboxes for "Mylist" and "Watchhistory"
            is_in_mylist = st.checkbox(f"Add {movie.movie_name} to Mylist", value=movie.in_mylist, key=f"mylist_{movie.movie_id}")
            is_in_watch_history = st.checkbox(f"Add {movie.movie_name} to Watchhistory", value=movie.in_watch_history, key=f"watchhistory_{movie.movie_id}")

            # Logic for "Mylist" checkbox
            handle_mylist_logic(mylist_service, user_id, movie.movie_id, movie.movie_name, is_in_mylist, movie.in_mylist)

            # Logic for "Watchhistory" checkbox
            handle_watch_history_logic(watch_history_service, user_id, movie.movie_id, movie.movie_name, is_in_watch_history, movie.in_watch_history)


def intersect_results(result_sets: list) -> pd.DataFrame:
    """
    Intersects the result sets of different queries to find common movies across filters.

    Args:
        result_sets (list): A list of DataFrames, each representing results from different filters.

    Returns:
        pd.DataFrame: The DataFrame containing movies common to all filter criteria.
    """
    if result_sets[0].empty:
        return pd.DataFrame()

    common_movie_ids = set(result_sets[0]["movie_id"])

    for df in result_sets[1:]:
        if df.empty:
            return pd.DataFrame()
        common_movie_ids &= set(df["movie_id"])

    filtered_dfs = [df[df["movie_id"].isin(common_movie_ids)] if not df.empty else df for df in result_sets]
    combined_movies = pd.concat(filtered_dfs).drop_duplicates(subset="movie_id")
    combined_movies.index = combined_movies['movie_id']
    combined_movies.drop(columns='_sa_instance_state', inplace=True)
    return combined_movies


def update_with_user_data(filtered_movies_df: pd.DataFrame, user_id: int):
    """
    Updates the DataFrame with user-specific data, such as whether a movie is in "Mylist" or "Watchhistory".

    Args:
        filtered_movies_df (pd.DataFrame): The DataFrame containing the filtered movies to update.
        user_id (int): The ID of the current user.

    Returns:
        None
    """
    watch_history_service = WatchHistoryService()
    mylist_service = MylistService()
    
    filtered_movies_df["in_watch_history"] = watch_history_service.is_in_watchhistory(user_id=user_id, movie_ids=filtered_movies_df["movie_id"])
    filtered_movies_df["in_mylist"] = mylist_service.is_in_mylist(user_id=user_id, movie_ids=filtered_movies_df["movie_id"])


def handle_mylist_logic(mylist_service, user_id: int, movie_id: int, movie_name: str, is_in_mylist: bool, original_in_mylist: bool):
    """
    Handles the logic for adding or removing a movie from the "Mylist".

    Args:
        mylist_service (MylistService): An instance of MylistService.
        user_id (int): The ID of the current user.
        movie_id (int): The ID of the movie being added/removed.
        movie_name (str): The name of the movie being added/removed.
        is_in_mylist (bool): Whether the movie is currently in the user's Mylist.
        original_in_mylist (bool): The initial state of the movie in the user's Mylist.

    Returns:
        None
    """
    if is_in_mylist and not original_in_mylist:
        mylist_service.create_mylist(user_id=user_id, movie_id=movie_id)
        st.success(f"Added {movie_name} to your Mylist.")
    elif not is_in_mylist and original_in_mylist:
        mylist_service.delete_mylist(user_id=user_id, movie_id=movie_id)
        st.success(f"Removed {movie_name} from your Mylist.")


def handle_watch_history_logic(watch_history_service, user_id: int, movie_id: int, movie_name: str, is_in_watch_history: bool, original_in_watch_history: bool):
    """
    Handles the logic for adding or removing a movie from the "Watchhistory".

    Args:
        watch_history_service (WatchHistoryService): An instance of WatchHistoryService.
        user_id (int): The ID of the current user.
        movie_id (int): The ID of the movie being added/removed.
        movie_name (str): The name of the movie being added/removed.
        is_in_watch_history (bool): Whether the movie is currently in the user's Watchhistory.
        original_in_watch_history (bool): The initial state of the movie in the user's Watchhistory.

    Returns:
        None
    """
    if is_in_watch_history and not original_in_watch_history:
        watch_history_service.create_watch_history(user_id=user_id, movie_id=movie_id, watch_date=datetime.now())
        st.success(f"Added {movie_name} to your Watchhistory.")
    elif not is_in_watch_history and original_in_watch_history:
        watch_history_service.delete_watch_history(user_id=user_id, movie_id=movie_id)
        st.success(f"Removed {movie_name} from your Watchhistory.")
