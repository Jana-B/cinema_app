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
   - Each result includes clickable links (if supported) to the movie details page for 
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
from app.services.user import UserService 
from datetime import datetime



def show_movie_search_page(user_id: int):
    # Instantiate the MovieService    
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
        # List to hold individual query results
        result_sets = execute_queries(movie_service, search_query, selected_genres, selected_persons, selected_studios, selected_keywords)

        # Find the intersection of all result sets (common movies across filters)
        if not result_sets[0].empty:
            filtered_movies_df = intersect_results(result_sets)

            # Display Results
            if not filtered_movies_df.empty: 
                watch_history_service = WatchHistoryService()
                mylist_service = MylistService()                                 
                filtered_movies_df["in_watch_history"] = watch_history_service.is_in_watchhistory(user_id=user_id,movie_ids=filtered_movies_df["movie_id"]) 
                filtered_movies_df["in_mylist"] = mylist_service.is_in_mylist(user_id=user_id,movie_ids=filtered_movies_df["movie_id"])         
                display_search_result(filtered_movies_df) 
                
                st.session_state['last_search_result'] = filtered_movies_df                                
            
            else:
                st.write("No movies found with the selected criteria.")
                
                
    elif 'last_search_result' in st.session_state:        
        watch_history_service = WatchHistoryService()
        mylist_service = MylistService()
        filtered_movies_df = st.session_state['last_search_result']
        filtered_movies_df["in_watch_history"] = watch_history_service.is_in_watchhistory(user_id=user_id,movie_ids=filtered_movies_df["movie_id"]) 
        filtered_movies_df["in_mylist"] = mylist_service.is_in_mylist(user_id=user_id,movie_ids=filtered_movies_df["movie_id"])         
        display_search_result(st.session_state['last_search_result'])
    
   

def execute_queries(movie_service, search_query, selected_genres, selected_persons, selected_studios, selected_keywords):
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

def display_search_result(filtered_movies_df):
    mylist_service = MylistService()
    watch_history_service = WatchHistoryService()
    # Initialize an empty string to hold the HTML content
    html_content = ""

    user_id = 0
    
    if 'user_id' in st.session_state:
        user_id = st.session_state['user_id']
    
    # Iterate through the DataFrame and create HTML content
    for movie in filtered_movies_df.itertuples():
        
        # movie_details_url = f"/?page=movie_details&movie_id={movie.movie_id}"
        movie_details_url = f"/?page=movie_details&movie_id={movie.movie_id}&user_id={user_id}"
        html_content = f"""
        <div style='margin-bottom: 20px;'>
            <h3><a href="{movie_details_url}" target="_self">{movie.movie_name}</a></h3>
            <p><strong>Release Date:</strong> {movie.movie_release_date}</p>
            <p><strong>Summary:</strong> {movie.movie_summary}</p>
        </div>
        """     
        html_content += "<hr>"
           
         # Display the checkboxes for "Mylist" and "Watchhistory"
        if user_id != 0:
            is_in_mylist = st.checkbox(f"Add {movie.movie_name} to Mylist", value=movie.in_mylist, key=f"mylist_{movie.movie_id}")
            is_in_watch_history = st.checkbox(f"Add {movie.movie_name} to Watchhistory", value=movie.in_watch_history, key=f"watchhistory_{movie.movie_id}")
        
        
        st.markdown(html_content, unsafe_allow_html=True)    

        # Handle the logic for "Mylist" checkbox
        if is_in_mylist and not movie.in_mylist:
            # Call the function to add the movie to Mylist
            mylist_service.create_mylist(user_id=user_id, movie_id=movie.movie_id)
            st.success(f"Added {movie.movie_name} to your Mylist.")
        elif not is_in_mylist and movie.in_mylist:
            mylist_service.delete_mylist(user_id=user_id, movie_id=movie.movie_id)
            st.success(f"Removed {movie.movie_name} from your Mylist.")

        # Handle the logic for "Watchhistory" checkbox
        if is_in_watch_history and not movie.in_watch_history:
            # Call the function to add the movie to Watchhistory
            current_date = datetime.now()
            watch_history_service.create_watch_history(user_id=user_id, movie_id=movie.movie_id, watch_date=current_date)
            st.success(f"Added {movie.movie_name} to your Watchhistory.")
        elif not is_in_watch_history and movie.in_watch_history:
            watch_history_service.delete_watch_history(user_id=user_id, movie_id=movie.movie_id)
            st.success(f"Removed {movie.movie_name} from your Watchhistory.")



def intersect_results(result_sets):
    
    if result_sets[0].empty:
        return
    
    common_movie_ids = set(result_sets[0]["movie_id"])

    
    
    # Intersect the movie_ids with those in the other DataFrames
    for df in result_sets[1:]:
        if df.empty:
            common_movie_ids = set()            
            return pd.DataFrame()
        else:
            common_movie_ids &= set(df["movie_id"])
  

    # Filter each DataFrame in result_sets to keep only the rows with common movie_ids
    filtered_dfs = [df[df["movie_id"].isin(common_movie_ids)] if not df.empty else df for df in result_sets]


    # Combine the filtered DataFrames into one
    combined_movies = pd.concat(filtered_dfs).drop_duplicates(subset="movie_id")
    
    combined_movies.index = combined_movies['movie_id']
    combined_movies.drop(columns='_sa_instance_state', inplace=True)
    return combined_movies
