import streamlit as st
import pandas as pd
from app.services.watchhistory import WatchHistoryService
from app.services.movie import MovieService

def show_dataframe_with_buttons(df):
    # Display the DataFrame in the data editor
    edited_df = st.data_editor(df, hide_index=False)
    
    # Create a button for each row outside of st.data_editor
    st.write("Actions:")
    for index, row in edited_df.iterrows():
        if st.button(f"Action for {row['Name']}", key=index):
            st.write(f"Button clicked for {row['Name']}")

            # Example action: you could process this row further or update the DataFrame
            # For instance, you could add a new column based on the button click:
            # edited_df.loc[index, 'Action'] = 'Clicked'

    # Display the updated DataFrame
    st.write("Updated DataFrame:")
    st.write(edited_df)



def show_watch_history_page(user_id: int):        
    watch_history_service = WatchHistoryService()
    movie_service = MovieService()

    # Read the user's watch history and movie names
    user_watch_history_df = watch_history_service.read_user_watch_history(user_id)  
    user_watch_history_df['movie_name'] = movie_service.read_movie_names(user_watch_history_df['movie_id'])
    
    # Display relevant columns for editing
    display_df = user_watch_history_df[['movie_name', 'watch_date', 'rating', 'is_favorite']].copy()    

    edit_df = st.data_editor(display_df, hide_index=True)

    # Check for differences between the original and edited DataFrame
    if not edit_df.equals(display_df) and st.button("Update Watch History"):
        st.write("Changes detected!")

        # Find the differences between the DataFrames
        df_diff = edit_df.compare(display_df)

        # Update the database with changes
        for index, row in df_diff.iterrows():
            movie_id = user_watch_history_df.loc[index, 'movie_id']

            # Check if rating has changed
            new_rating = edit_df.loc[index, 'rating'] if 'rating' in df_diff.columns.get_level_values(0) else None

            # Check if is_favorite has changed
            new_is_favorite = edit_df.loc[index, 'is_favorite'] if 'is_favorite' in df_diff.columns.get_level_values(0) else None

            # Update the watch history in the database
            watch_history_service.update_watch_history(
                user_id=int(user_id),
                movie_id=int(movie_id),
                rating=new_rating,
                is_favorite=new_is_favorite
            )

        st.success("Watch history updated successfully!")
    
