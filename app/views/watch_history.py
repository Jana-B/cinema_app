from datetime import datetime, date
import streamlit as st
import pandas as pd
from app.services.watchhistory import WatchHistoryService
from app.services.mylist import MylistService
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
    mylist_service = MylistService()
        
    movie_service = MovieService()

    # Read the user's watch history and movie names
    user_watch_history_df = watch_history_service.read_user_watch_history(user_id)  
    user_watch_history_df['in_watch_history'] = True
    
    mylist_df = mylist_service.read_user_mylist(user_id)
    mylist_df['in_mylist'] = True
    
    if not user_watch_history_df.empty and not mylist_df.empty:    
        mylist_only_movie_ids = mylist_df[~mylist_df['movie_id'].isin(user_watch_history_df['movie_id'])]        
        consolidated_df = pd.concat([user_watch_history_df, mylist_only_movie_ids], ignore_index=True)    
        consolidated_df['in_mylist'] = consolidated_df['movie_id'].isin(mylist_df['movie_id'])
        
    elif not user_watch_history_df.empty and mylist_df.empty:
        consolidated_df = user_watch_history_df
        consolidated_df['in_mylist'] = False
    elif user_watch_history_df.empty and not mylist_df.empty:
        consolidated_df = mylist_df
        consolidated_df['in_watch_history'] = False
        consolidated_df['rating']  = 0
        consolidated_df['watch_date'] = None
        consolidated_df['is_favorite']  = None
                        
    if consolidated_df.empty:
        st.write('No watch history and no mylist data')
        return
        
    consolidated_df['movie_name'] = movie_service.read_movie_names(consolidated_df['movie_id'])
    
    # Display relevant columns for editing    
    display_df = consolidated_df[['movie_name', 'watch_date', 'in_watch_history', 'in_mylist', 'rating', 'is_favorite']].copy()    


    # for index, row in display_df.iterrows():
    #     st.write(row.movie_name, row.watch_date, row.rating, row.is_favorite)
    # Iterate through each row and use a slider for the rating field
    
    # Create two main columns: one for the DataFrame, one for the feedback
    # col1, col2 = st.columns([3, 1])  # Adjust column widths as needed
    new_ratings = []
    
    # with col1:
    # # Display the DataFrame excluding the 'rating' column
    #     st.write("Movie List:")
    #     st.data_editor(consolidated_df[['movie_name', 'watch_date', 'in_watch_history', 'in_mylist', 'is_favorite']], hide_index=True)

    # with col2:
        # Show feedback UI elements in a column aligned with the DataFrame rows
    st.write("Feedback (Ratings)")
    
    
    initial_date = pd.Timestamp('1970-01-01')
    consolidated_df['watch_date'].fillna(initial_date, inplace=True)
    
    for index, row in consolidated_df.iterrows():
        st.header(row['movie_name'])
        movie_name = row['movie_name']
        movie_id = row['movie_id']
        watch_date = row['watch_date']
        in_watch_history = row['in_watch_history']
        in_mylist = row['in_mylist']
        is_favorite = row['is_favorite']
        if pd.isna(row['rating']):
            rating = 1
        else:
            rating = row['rating']
        
        
        new_watch_date = st.date_input(label='Watch Date', value=row['watch_date'], key=f"watch_date_{row['movie_id']}")
        new_in_watch_history = st.checkbox(label='In Watch History', value=row['in_watch_history'], key=f"in_watch_history_{row['movie_id']}")
        new_in_mylist = st.checkbox(label='In My List', value=row['in_mylist'], key=f"in_mylist_{row['movie_id']}")
        new_is_favorite = st.checkbox(label='Favorite', value=row['is_favorite'], key=f"is_favorite_{row['movie_id']}")
                
        
        new_rating = st.slider('Rating (Stars)', min_value=1, max_value=5, value=int(rating), format="%d ⭐", key=f"rating_{row['movie_id']}")
        
        
        # Handle the logic for "Watchhistory" checkbox
        if new_in_watch_history and not in_watch_history:
            # Call the function to add the movie to Watchhistory
            if pd.isna(watch_date):            
                watch_date = datetime.now()                                
            watch_history_service.create_watch_history(user_id=int(user_id), 
                                                        movie_id=int(movie_id), 
                                                        watch_date=watch_date,
                                                        rating=new_rating,
                                                        is_favorite=new_is_favorite)
            st.success(f"Added {movie_name} to your Watchhistory.")            
        elif not new_in_watch_history and in_watch_history:
            watch_history_service.delete_watch_history(user_id=int(user_id), movie_id=int(movie_id))
            st.success(f"Removed {movie_name} from your Watchhistory.")                        
            
            
        # Handle the logic for "Mylist" checkbox
        if new_in_mylist and not in_mylist:
            # Call the function to add the movie to Mylist
            mylist_service.create_mylist(user_id=int(user_id), movie_id=int(movie_id))
            st.success(f"Added {movie_name} to your Mylist.")
        elif not new_in_mylist and in_mylist:
            mylist_service.delete_mylist(user_id=int(user_id), movie_id=int(movie_id))
            st.success(f"Removed {movie_name} from your Mylist.")

        
        if new_watch_date != watch_date or new_is_favorite != is_favorite or new_rating != rating and new_in_watch_history:
           watch_history_service.update_watch_history(
                user_id=int(user_id),
                movie_id=int(movie_id),
                watch_date=new_watch_date,
                rating=new_rating,
                is_favorite=new_is_favorite
            ) 
           

    # Update the 'rating' column with the new ratings
    # consolidated_df['rating'] = new_ratings
  
    #   edit_df = st.data_editor(display_df, hide_index=True)

    if st.button('Delete Watch History'):
        watch_history_service.delete_complete_watch_history(user_id)


    # Check for differences between the original and edited DataFrame
    # if not edit_df.equals(display_df) and st.button("Update Watch History"):
    #     st.write("Changes detected!")

    #     # Find the differences between the DataFrames
    #     df_diff = edit_df.compare(display_df)

    #     # Update the database with changes
    #     for index, row in df_diff.iterrows():
    #         movie_id = consolidated_df.loc[index, 'movie_id']            
    #         movie_name = consolidated_df.loc[index, 'movie_name']
    #         old_is_in_mylist = consolidated_df.loc[index, 'in_mylist']
    #         old_is_in_watch_history = consolidated_df.loc[index, 'in_watch_history']

    #         # Check if rating has changed
    #         new_rating = edit_df.loc[index, 'rating'] if 'rating' in df_diff.columns.get_level_values(0) else None

    #         # Check if is_favorite has changed
    #         new_is_favorite = edit_df.loc[index, 'is_favorite'] if 'is_favorite' in df_diff.columns.get_level_values(0) else None
            
    #         watch_date = edit_df.loc[index, 'watch_date']
            

    #         # Update the watch history in the database
    #         watch_history_service.update_watch_history(
    #             user_id=int(user_id),
    #             movie_id=int(movie_id),
    #             watch_date=watch_date,
    #             rating=new_rating,
    #             is_favorite=new_is_favorite
    #         )
            
    #         new_in_mylist = edit_df.loc[index, 'in_mylist'] if 'in_mylist' in df_diff.columns.get_level_values(0) else None
            
    #        # Handle the logic for "Mylist" checkbox
    #         if new_in_mylist is not None and new_in_mylist:
    #             # Call the function to add the movie to Mylist
    #             mylist_service.create_mylist(user_id=int(user_id), movie_id=int(movie_id))
    #             st.success(f"Added {movie_name} to your Mylist.")
    #         elif new_in_mylist is not None and not new_in_mylist and old_is_in_mylist:
    #             mylist_service.delete_mylist(user_id=int(user_id), movie_id=int(movie_id))
    #             st.success(f"Removed {movie_name} from your Mylist.")

    #         new_in_watch_history = edit_df.loc[index, 'in_watch_history'] if 'in_watch_history' in df_diff.columns.get_level_values(0) else None
            
    #         # Handle the logic for "Watchhistory" checkbox
    #         if new_in_watch_history is not None and new_in_watch_history:
    #             # Call the function to add the movie to Watchhistory
    #             if pd.isna(watch_date):            
    #                 watch_date = datetime.now()                                
    #             watch_history_service.create_watch_history(user_id=int(user_id), 
    #                                                        movie_id=int(movie_id), 
    #                                                        watch_date=watch_date,
    #                                                        rating=new_rating,
    #                                                        is_favorite=new_is_favorite)
    #             st.success(f"Added {movie_name} to your Watchhistory.")
    #         elif new_in_watch_history is not None and not new_in_watch_history and old_is_in_watch_history:
    #             watch_history_service.delete_watch_history(user_id=int(user_id), movie_id=int(movie_id))
    #             st.success(f"Removed {movie_name} from your Watchhistory.")

    #     st.success("Watch history updated successfully!")
    
