import streamlit as st
from app.views import movie_search, movie_details

def main():
    try:
        page = st.query_params.page
        movie_id = st.query_params.movie_id
    except Exception as e:                
        page = None
        movie_id = None
        
        
        
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", [
        "Movie Search", "User Creation", "Movie Rating", "Watchlist", "Personal List", "Profile"
    ])

    if selected_page == "Movie Search":
        movie_search.show_movie_search_page()
    elif selected_page == "User Creation":
        # user_creation.show_user_creation_page()
        pass
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
