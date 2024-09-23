"""
Module for managing and displaying a user's watch history and movie list in a Streamlit application.

This module provides functionality to:
- Display a consolidated view of the user's watch history and "My List" movies.
- Allow the user to interactively update the watch history and movie list (e.g., adding/removing movies, updating ratings).
- Handle changes such as adding/removing movies to/from the watch history or "My List".
- Provide a mechanism for the user to delete the entire watch history.

Dependencies:
- `WatchHistoryService`: Manages operations related to the user's watch history.
- `MylistService`: Manages operations related to the user's movie list.
- `MovieService`: Provides access to movie data (e.g., movie names).

Functions:
- `show_my_lists_page`: Displays the main page for managing the user's watch history and movie list.
- `display_movie_entry`: Renders the interactive UI for a single movie.
- `handle_watch_history_update`: Handles the logic for updating the watch history.
- `handle_mylist_update`: Handles the logic for updating the user's movie list.
- `get_consolidated_dataframe`: Merges watch history and movie list data into a consolidated DataFrame for display and interaction.
"""
import math
from datetime import datetime
import streamlit as st
import pandas as pd
from app.services.watchhistory import WatchHistoryService
from app.services.mylist import MylistService
from app.services.movie import MovieService

def show_my_lists_page(user_id: int):
    """
    Displays the main page for managing the user's watch history and "My List".

    This function sets up the title and checks if there is any data to display.
    If there is no watch history or "My List" data for the user, it shows a message.
    Otherwise, it renders the consolidated movie data in an interactive interface.

    Args:
        user_id (int): The unique identifier of the user.
    """
    watch_history_service = WatchHistoryService()
    mylist_service = MylistService()
    movie_service = MovieService()

    # Get consolidated user data
    consolidated_df = get_consolidated_dataframe(user_id, watch_history_service, mylist_service, movie_service)
    
    st.title("Watch History and My List")
    
    if consolidated_df.empty:
        st.write("No watch history and no mylist data.")
        return        

    display_consolidated_lists(user_id, watch_history_service, mylist_service, consolidated_df)

def display_consolidated_lists(user_id: int, watch_history_service, mylist_service, consolidated_df: pd.DataFrame):
    """
    Displays and handles the interaction for the consolidated watch history and "My List".

    For each movie in the consolidated DataFrame, this function displays the movie name,
    allows the user to edit watch date, rating, and favorite status, and provides checkboxes
    for adding/removing the movie to/from the watch history and "My List".

    Args:
        user_id (int): The unique identifier of the user.
        watch_history_service (WatchHistoryService): Service for managing watch history.
        mylist_service (MylistService): Service for managing the "My List".
        consolidated_df (pd.DataFrame): The consolidated DataFrame containing movies in the watch history and "My List".
    """
    for _, row in consolidated_df.iterrows():
        display_movie_entry(user_id, row, watch_history_service, mylist_service)

    if st.button("Delete Watch History"):
        watch_history_service.delete_complete_watch_history(user_id)

def display_movie_entry(user_id: int, movie_data: pd.Series, watch_history_service, mylist_service):
    """
    Displays a single movie entry with interactive fields for editing watch history, 
    "My List" status, rating, and favorite status.

    Args:
        user_id (int): The unique identifier of the user.
        movie_data (pd.Series): Series containing the movie's details from the consolidated DataFrame.
        watch_history_service (WatchHistoryService): Service for managing watch history.
        mylist_service (MylistService): Service for managing the "My List".
    """
    movie_name = movie_data["movie_name"]
    movie_id = movie_data["movie_id"]
    
    
    rating = movie_data.get("rating", 1)
    if math.isnan(rating):
        rating = 1  # Set default rating if NaN

    # Display movie name as header
    st.header(movie_name)

    # Display interactive fields
    new_watch_date = st.date_input(
        "Watch Date", value=movie_data["watch_date"], key=f"watch_date_{movie_id}"
    )
    new_in_watch_history = st.checkbox(
        "In Watch History", value=movie_data["in_watch_history"], key=f"in_watch_history_{movie_id}"
    )
    new_in_mylist = st.checkbox(
        "In My List", value=movie_data["in_mylist"], key=f"in_mylist_{movie_id}"
    )
    new_is_favorite = st.checkbox(
        "Favorite", value=movie_data["is_favorite"], key=f"is_favorite_{movie_id}"
    )
    new_rating = st.slider(
        "Rating (Stars)", min_value=1, max_value=5, value=int(rating),
        format="%d ⭐", key=f"rating_{movie_id}"
    )

    # Update watch history and "My List" based on user input
    handle_watch_history_update(user_id, movie_data, watch_history_service, new_in_watch_history, new_watch_date, new_rating, new_is_favorite)
    handle_mylist_update(user_id, movie_data, mylist_service, new_in_mylist)

def handle_watch_history_update(user_id: int, movie_data: pd.Series, watch_history_service, in_watch_history: bool, watch_date, rating, is_favorite):
    """
    Handles the logic for adding, updating, or removing a movie in the user's watch history.

    Args:
        user_id (int): The unique identifier of the user.
        movie_data (pd.Series): Series containing the movie's details from the consolidated DataFrame.
        watch_history_service (WatchHistoryService): Service for managing watch history.
        in_watch_history (bool): Indicates whether the movie is in the watch history.
        watch_date (datetime): The date the movie was watched.
        rating (int): The user's rating for the movie.
        is_favorite (bool): Indicates if the movie is marked as a favorite.
    """
    movie_id = movie_data["movie_id"]
    prev_in_watch_history = movie_data["in_watch_history"]

    if in_watch_history and not prev_in_watch_history:
        # Add movie to watch history
        watch_history_service.create_watch_history(user_id, movie_id, watch_date or datetime.now(), rating, is_favorite)
        st.success(f"Added {movie_data['movie_name']} to your Watch History.")
    elif not in_watch_history and prev_in_watch_history:
        # Remove movie from watch history
        watch_history_service.delete_watch_history(user_id, movie_id)
        st.success(f"Removed {movie_data['movie_name']} from your Watch History.")
    elif in_watch_history:
        # Update watch history if any changes are made
        watch_history_service.update_watch_history(user_id, movie_id, watch_date, rating, is_favorite)

def handle_mylist_update(user_id: int, movie_data: pd.Series, mylist_service, in_mylist: bool):
    """
    Handles the logic for adding or removing a movie in the user's "My List".

    Args:
        user_id (int): The unique identifier of the user.
        movie_data (pd.Series): Series containing the movie's details from the consolidated DataFrame.
        mylist_service (MylistService): Service for managing the "My List".
        in_mylist (bool): Indicates whether the movie is in the "My List".
    """
    movie_id = movie_data["movie_id"]
    prev_in_mylist = movie_data["in_mylist"]

    if in_mylist and not prev_in_mylist:
        # Add movie to My List
        mylist_service.create_mylist(user_id, movie_id)
        st.success(f"Added {movie_data['movie_name']} to your My List.")
    elif not in_mylist and prev_in_mylist:
        # Remove movie from My List
        mylist_service.delete_mylist(user_id, movie_id)
        st.success(f"Removed {movie_data['movie_name']} from your My List.")

def get_consolidated_dataframe(user_id: int, watch_history_service, mylist_service, movie_service) -> pd.DataFrame:
    """
    Retrieves and consolidates the user's watch history and "My List" data into a single DataFrame.

    Args:
        user_id (int): The unique identifier of the user.
        watch_history_service (WatchHistoryService): Service for managing watch history.
        mylist_service (MylistService): Service for managing the "My List".
        movie_service (MovieService): Service for retrieving movie details.

    Returns:
        pd.DataFrame: A consolidated DataFrame containing the user's watch history and "My List".
    """
    user_watch_history_df = watch_history_service.read_user_watch_history(user_id)
    user_watch_history_df["in_watch_history"] = True

    mylist_df = mylist_service.read_user_mylist(user_id)
    mylist_df["in_mylist"] = True

    if not user_watch_history_df.empty and not mylist_df.empty:
        # Combine watch history and My List data, avoiding duplicates
        mylist_only_movie_ids = mylist_df[~mylist_df["movie_id"].isin(user_watch_history_df["movie_id"])]
        consolidated_df = pd.concat([user_watch_history_df, mylist_only_movie_ids], ignore_index=True)
        consolidated_df["in_mylist"] = consolidated_df["movie_id"].isin(mylist_df["movie_id"])
    elif not user_watch_history_df.empty:
        consolidated_df = user_watch_history_df
        consolidated_df["in_mylist"] = False
    elif not mylist_df.empty:
        consolidated_df = mylist_df
        consolidated_df["in_watch_history"] = False
        consolidated_df["rating"] = 0
        consolidated_df["watch_date"] = None
        consolidated_df["is_favorite"] = None
    else:
        return pd.DataFrame()  # Return empty DataFrame if no data

    # Retrieve movie names and fill missing watch dates with a default value
    consolidated_df["movie_name"] = movie_service.read_movie_names(consolidated_df["movie_id"])
    consolidated_df["watch_date"].fillna(pd.Timestamp("1970-01-01"), inplace=True)

    return consolidated_df
