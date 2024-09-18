import streamlit as st
from app.views import movie_search, movie_details, user_management, watch_history
from app.services.user import UserService

def main():
    user_service = UserService()
    
    selected_sub_page, movie_id, user_id = get_query_parmeter()
       
    if user_id == 0:
        user_id = get_session_user_id()   
    
    
    st.sidebar.title("Navigation")
    
    if user_id != 0:        
        user = user_service.read_user(user_id)
        st.sidebar.write(f"User: {user.user_name}")    
    
    # Input fields for user_name and password
    user_name = st.sidebar.text_input("User", placeholder="Enter your user name")
    password = st.sidebar.text_input("Password", placeholder="Enter your password", type="password")

    # Button to execute login
    login_button = st.sidebar.button("Login")

    # Logic to execute when login button is clicked
    if login_button:        
        if user_name and password and user_service.verify_user(user_name=user_name, password=password):
            user_id = user_service.get_id_by_name(user_name)
            st.session_state["user_id"] = user_id
            st.session_state["user_name"] = user_name
            st.sidebar.success("Login successful!")
        else:
            st.sidebar.error("User name or password not vallid")
    elif user_id == 0:
        st.sidebar.error("Please enter both email and password.")
        
    selected_page = st.sidebar.radio("Go to", [
        "Movie Search", "User Profile", "Movie Rating", "Watch History", "Personal List", "Profile"
    ])

    if selected_page == "Movie Search":
        movie_search.show_movie_search_page(user_id=user_id)
        
    elif selected_page == "User Profile":
        user_management.show_user_management_page()
        
    elif selected_page == "Movie Rating":
        # movie_rating.show_movie_rating_page()
        pass
    elif selected_page == "Watch History":
        watch_history.show_watch_history_page(user_id)        
    elif selected_page == "Personal List":
        # personal_list.show_personal_list_page()
        pass
    elif selected_page == "Profile":
        # profile.show_profile_page()
        pass
    
    # Check for movie_details page in query parameters
    if selected_sub_page == "movie_details":       
        movie_details.show_movie_details_page(movie_id, user_id)

def get_query_parmeter():
    try:
        user_id = int(st.query_params.user_id)
    except Exception as e:                
        user_id = 0        
    
    try:
        page = st.query_params.page
        movie_id = int(st.query_params.movie_id)
    except Exception as e:                
        page = ''
        movie_id = 0
                
    return page,movie_id,user_id

def get_session_user_id():
    if 'user_id' in  st.session_state:
        user_id = st.session_state.user_id
    else:
        user_id = 0
        
    return user_id
        
        

if __name__ == "__main__":
    main()
