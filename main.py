import streamlit as st
from app.views import movie_search, movie_details, user_management
from app.services.user import UserService

def main():
    try:
        page = st.query_params.page
        movie_id = st.query_params.movie_id
    except Exception as e:                
        page = None
        movie_id = None
        
        
        
    st.sidebar.title("Navigation")
    
    # Input fields for user_name and password
    user_name = st.sidebar.text_input("User", placeholder="Enter your user name")
    password = st.sidebar.text_input("Password", placeholder="Enter your password", type="password")

    # Button to execute login
    login_button = st.sidebar.button("Login")

    # Logic to execute when login button is clicked
    if login_button:
        user_service = UserService()
        if user_name and password and user_service.verify_user(user_name=user_name, password=password):
            st.session_state["user_name"] = user_name
            st.sidebar.success("Login successful!")
        else:
            st.sidebar.error("User name or password not vallid")
    else:
        st.sidebar.error("Please enter both email and password.")
        
    selected_page = st.sidebar.radio("Go to", [
        "Movie Search", "User Profile", "Movie Rating", "Watchlist", "Personal List", "Profile"
    ])

    if selected_page == "Movie Search":
        movie_search.show_movie_search_page()
        
    elif selected_page == "User Profile":
        user_management.show_user_management_page()
        
    elif selected_page == "Movie Rating":
        # movie_rating.show_movie_rating_page()
        pass
    elif selected_page == "Watchlist":
        # watchlist.show_watchlist_page()
        pass
    elif selected_page == "Personal List":
        # personal_list.show_personal_list_page()
        pass
    elif selected_page == "Profile":
        # profile.show_profile_page()
        pass
    
    # Check for movie_details page in query parameters
    if page == "movie_details":
        # integrate movie_id into interface....
        movie_details.show_movie_details_page(movie_id)
        
        

if __name__ == "__main__":
    main()
