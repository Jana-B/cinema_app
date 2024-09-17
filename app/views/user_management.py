import streamlit as st
from datetime import date
from app.services.user import UserService

def show_user_management_page():
    st.title("User Management")

    user_service = UserService()

    # Option to select user action
    action = st.selectbox("Choose Action", ["Create User", "View Users", "Update User", "Delete User"])

    # Create User
    if action == "Create User":
        st.header("Create a New User")
        user_name = st.text_input("User Name")
        birthdate = st.date_input(label= "Birthdate", min_value=date(1900,1,1), max_value = date(2017,1,1), value = None)
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        
        if st.button("Create User"):
            if user_name and birthdate and password and email:
                try:
                    user_service.create_user(user_name, birthdate, password, email)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    #st.error(f"User '{user_name}' already exists!")
                    return
                st.success(f"User '{user_name}' created successfully!")
                
            else:
                st.error("All fields are required to create a user.")
    
    # View Users
    elif action == "View Users":
        st.header("View All Users")
        users_df = user_service.read_all_users()
        st.dataframe(users_df)

    # Update User
    elif action == "Update User":
        st.header("Update an Existing User")
        user_id = st.number_input("User ID", min_value=1, step=1)
        if user_id:
            user = user_service.read_user(user_id)
            if user:
                user_name = st.text_input("User Name", value=user.user_name)
                birthdate = st.date_input("Birthdate", value=user.user_birthdate, min_value=date(1900,1,1))
                password = st.text_input("Password", value=user.password, type="password")
                email = st.text_input("Email", value=user.e_mail)

                if st.button("Update User"):
                    user_service.update_user(user_id, user_name=user_name, birthdate=birthdate, password=password, e_mail=email)
                    st.success(f"User '{user_name}' updated successfully!")
            else:
                st.error("User not found.")
    
    # Delete User
    elif action == "Delete User":
        st.header("Delete a User")
        user_id = st.number_input("User ID to delete", min_value=1, step=1)
        if user_id:
            user = user_service.read_user(user_id)
            if user:
                if st.button("Delete User"):
                    user_service.delete_user(user_id)
                    st.success(f"User ID '{user_id}' deleted successfully!")
            else:
                st.error("User not found.")
