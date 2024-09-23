from datetime import datetime, date
import streamlit as st
import pandas as pd
from app.services.watchhistory import WatchHistoryService
from app.services.mylist import MylistService
from app.services.movie import MovieService


def show_my_lists_page(user_id: int):
    
    watch_history_service = WatchHistoryService()
    mylist_service = MylistService()

    movie_service = MovieService()

    # Read the user's watch history and movie names
    consolidated_df = get_consolidated_dataframe(user_id, watch_history_service, mylist_service, movie_service)
    
    st.title("Watch History and My List")
    
    if consolidated_df.empty:
        st.write("No watch history and no mylist data")
        return        

    display_consolidated_lists(user_id, watch_history_service, mylist_service, consolidated_df)

def display_consolidated_lists(user_id, watch_history_service, mylist_service, consolidated_df):
    for index, row in consolidated_df.iterrows():
        st.header(row["movie_name"])
        movie_name = row["movie_name"]
        movie_id = row["movie_id"]
        watch_date = row["watch_date"]
        in_watch_history = row["in_watch_history"]
        in_mylist = row["in_mylist"]
        is_favorite = row["is_favorite"]
        if pd.isna(row["rating"]):
            rating = 1
        else:
            rating = row["rating"]

        new_watch_date = st.date_input(
            label="Watch Date",
            value=row["watch_date"],
            key=f"watch_date_{row['movie_id']}",
        )
        new_in_watch_history = st.checkbox(
            label="In Watch History",
            value=row["in_watch_history"],
            key=f"in_watch_history_{row['movie_id']}",
        )
        new_in_mylist = st.checkbox(
            label="In My List",
            value=row["in_mylist"],
            key=f"in_mylist_{row['movie_id']}",
        )
        new_is_favorite = st.checkbox(
            label="Favorite",
            value=row["is_favorite"],
            key=f"is_favorite_{row['movie_id']}",
        )

        new_rating = st.slider(
            "Rating (Stars)",
            min_value=1,
            max_value=5,
            value=int(rating),
            format="%d ⭐",
            key=f"rating_{row['movie_id']}",
        )

        # Handle the logic for "Watchhistory" checkbox
        if new_in_watch_history and not in_watch_history:
            # Call the function to add the movie to Watchhistory
            if pd.isna(watch_date):
                watch_date = datetime.now()
            watch_history_service.create_watch_history(
                user_id=int(user_id),
                movie_id=int(movie_id),
                watch_date=watch_date,
                rating=new_rating,
                is_favorite=new_is_favorite,
            )
            st.success(f"Added {movie_name} to your Watchhistory.")
        elif not new_in_watch_history and in_watch_history:
            watch_history_service.delete_watch_history(
                user_id=int(user_id), movie_id=int(movie_id)
            )
            st.success(f"Removed {movie_name} from your Watchhistory.")

        # Handle the logic for "Mylist" checkbox
        if new_in_mylist and not in_mylist:
            # Call the function to add the movie to Mylist
            mylist_service.create_mylist(user_id=int(user_id), movie_id=int(movie_id))
            st.success(f"Added {movie_name} to your Mylist.")
        elif not new_in_mylist and in_mylist:
            mylist_service.delete_mylist(user_id=int(user_id), movie_id=int(movie_id))
            st.success(f"Removed {movie_name} from your Mylist.")

        if (
            new_watch_date != watch_date
            or new_is_favorite != is_favorite
            or new_rating != rating
            and new_in_watch_history
        ):
            watch_history_service.update_watch_history(
                user_id=int(user_id),
                movie_id=int(movie_id),
                watch_date=new_watch_date,
                rating=new_rating,
                is_favorite=new_is_favorite,
            )

    if st.button("Delete Watch History"):
        watch_history_service.delete_complete_watch_history(user_id)

def get_consolidated_dataframe(user_id, watch_history_service, mylist_service, movie_service):
    user_watch_history_df = watch_history_service.read_user_watch_history(user_id)
    user_watch_history_df["in_watch_history"] = True

    mylist_df = mylist_service.read_user_mylist(user_id)
    mylist_df["in_mylist"] = True

    if not user_watch_history_df.empty and not mylist_df.empty:
        mylist_only_movie_ids = mylist_df[
            ~mylist_df["movie_id"].isin(user_watch_history_df["movie_id"])
        ]
        consolidated_df = pd.concat(
            [user_watch_history_df, mylist_only_movie_ids], ignore_index=True
        )
        consolidated_df["in_mylist"] = consolidated_df["movie_id"].isin(
            mylist_df["movie_id"]
        )

    elif not user_watch_history_df.empty and mylist_df.empty:
        consolidated_df = user_watch_history_df
        consolidated_df["in_mylist"] = False
    elif user_watch_history_df.empty and not mylist_df.empty:
        consolidated_df = mylist_df
        consolidated_df["in_watch_history"] = False
        consolidated_df["rating"] = 0
        consolidated_df["watch_date"] = None
        consolidated_df["is_favorite"] = None
    
    consolidated_df["movie_name"] = movie_service.read_movie_names(
        consolidated_df["movie_id"]
    )
    initial_date = pd.Timestamp("1970-01-01")
    consolidated_df["watch_date"].fillna(initial_date, inplace=True)
    return consolidated_df
