"""
main.py

This module serves as the main entry point for the movie recommendation app. It handles 
navigation between different pages, user authentication, and session management.

Features:
---------
1. **User Authentication**: 
- Provides a login mechanism through the sidebar, where users input their credentials 
  (username and password). 
- Displays user-specific information upon successful login.
  
2. **Page Navigation**:
- Users can navigate between different pages, such as "Movie Search", "My Lists", 
  and "User Profile", using radio buttons in the sidebar.
  
3. **Movie Details**:
- Automatically redirects to a movie details page based on query parameters from the URL.

Dependencies:
-------------
- Streamlit for UI components and layout management.
- `UserService` for handling user-related database queries.
- `movie_search`, `movie_details`, `my_lists`, and `user_management` for page-specific logic.
"""

import streamlit as st
from app.views import movie_search, movie_details, my_lists, user_management
from app.services.user import UserService


def main():
    """
    Main entry point of the application. Handles user login, session management, 
    and navigation between different app views.

    Returns:
        None
    """
    user_service = UserService()
    
    # Parse query parameters (e.g., movie_id, user_id, and page)
    selected_sub_page, movie_id, user_id = get_query_parameter()
    
    # If no user_id is passed, retrieve it from the session
    if user_id == 0:
        user_id = get_session_user_id()

    # Sidebar for navigation and user input
    st.sidebar.title("Navigation")
    
    if user_id != 0:
        user = user_service.read_user(user_id)
        st.sidebar.write(f"User: {user.user_name}")
    
    # User login fields and logic
    handle_user_login(user_service, user_id)

    # Page navigation
    selected_page = st.sidebar.radio("Go to", ["Movie Search", "My Lists", "User Profile"])
    navigate_to_page(selected_page, user_id, movie_id, selected_sub_page)


def handle_user_login(user_service: UserService, user_id: int):
    """
    Handles the user login logic, allowing users to input their username and password 
    and validating the credentials. Updates session state upon successful login.

    Args:
        user_service (UserService): An instance of the UserService for verifying user credentials.
        user_id (int): The ID of the user (0 if not logged in).

    Returns:
        None
    """
    # Input fields for username and password
    user_name = st.sidebar.text_input("User", placeholder="Enter your username")
    password = st.sidebar.text_input("Password", placeholder="Enter your password", type="password")

    # Login button
    login_button = st.sidebar.button("Login")

    # Handle login logic
    if login_button:
        if user_name and password and user_service.verify_user(user_name=user_name, password=password):
            user_id = user_service.get_id_by_name(user_name)
            st.session_state["user_id"] = user_id
            st.session_state["user_name"] = user_name
            st.sidebar.success("Login successful!")
        else:
            st.sidebar.error("Invalid username or password.")
    elif user_id == 0:
        st.sidebar.error("Please enter both username and password.")


def navigate_to_page(selected_page: str, user_id: int, movie_id: int, selected_sub_page: str):
    """
    Navigates to the selected page based on the user's choice from the sidebar and query parameters.

    Args:
        selected_page (str): The page selected from the sidebar navigation.
        user_id (int): The ID of the logged-in user (0 if not logged in).
        movie_id (int): The ID of the selected movie (if applicable).
        selected_sub_page (str): The sub-page indicated by the query parameters (e.g., "movie_details").

    Returns:
        None
    """
    # Handle navigation to "Movie Search", "My Lists", and "User Profile"
    if selected_page == "Movie Search":
        movie_search.show_movie_search_page(user_id=user_id)
    elif selected_page == "My Lists":
        my_lists.show_my_lists_page(user_id)
    elif selected_page == "User Profile":
        user_management.show_user_management_page()

    # Handle navigation to the movie details page based on query parameters
    if selected_sub_page == "movie_details":
        movie_details.show_movie_details_page(movie_id, user_id)


def get_query_parameter() -> tuple:
    """
    Retrieves the query parameters from the URL (user_id, movie_id, and page).

    Returns:
        tuple: A tuple containing the selected sub-page (str), movie_id (int), and user_id (int).
    """
    try:
        user_id = int(st.query_params.get('user_id', 0))
    except ValueError:
        user_id = 0

    try:
        page = st.query_params.get('page', '')
        movie_id = int(st.query_params.get('movie_id', 0))
    except ValueError:
        page = ''
        movie_id = 0

    return page, movie_id, user_id


def get_session_user_id() -> int:
    """
    Retrieves the user_id from the session state, if available.

    Returns:
        int: The user_id stored in the session (0 if not found).
    """
    return st.session_state.get('user_id', 0)


if __name__ == "__main__":
    main()
