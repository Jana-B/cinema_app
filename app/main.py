import streamlit as st
from app.views import movie_search
#user_creation, movie_rating, watchlist, personal_list, profile

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "Movie Search", "User Creation", "Movie Rating", "Watchlist", "Personal List", "Profile"
    ])
    
    if page == "Movie Search":
        movie_search.show_movie_search_page()
    # elif page == "User Creation":
    #     user_creation.show_user_creation_page()
    # elif page == "Movie Rating":
    #     movie_rating.show_movie_rating_page()
    # elif page == "Watchlist":
    #     watchlist.show_watchlist_page()
    # elif page == "Personal List":
    #     personal_list.show_personal_list_page()
    # elif page == "Profile":
    #     profile.show_profile_page()

if __name__ == "__main__":
    main()
