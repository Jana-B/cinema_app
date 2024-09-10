import streamlit as st
import pandas as pd
from services import MovieService  # Ensure MovieService is in movie_service.py or adjust import path

# Create an instance of MovieService
movie_service = MovieService()

st.title("Movie Database Search")

# Sidebar for filters
st.sidebar.header("Search Options")

search_type = st.sidebar.selectbox("Select search type", [
    "By Title",
    "By Genre",
    "By Release Date",
    "By Keyword",
    "By Person",
    "By Studio"
])

if search_type == "By Title":
    title = st.sidebar.text_input("Enter movie title")
    exact_match = st.sidebar.checkbox("Exact match")
    if st.sidebar.button("Search"):
        if title:
            results = movie_service.query_by_title(title, exact_match)
            st.dataframe(results)
        else:
            st.error("Please enter a movie title.")

elif search_type == "By Genre":
    genre = st.sidebar.text_input("Enter genre")
    if st.sidebar.button("Search"):
        if genre:
            results = movie_service.query_by_genre(genre)
            st.dataframe(results)
        else:
            st.error("Please enter a genre.")

elif search_type == "By Release Date":
    start_date = st.sidebar.date_input("Start date")
    end_date = st.sidebar.date_input("End date")
    if st.sidebar.button("Search"):
        results = movie_service.query_by_release_date(start_date, end_date)
        st.dataframe(pd.DataFrame([movie.__dict__ for movie in results]))

elif search_type == "By Keyword":
    keyword = st.sidebar.text_input("Enter keyword")
    if st.sidebar.button("Search"):
        if keyword:
            results = movie_service.query_by_keyword(keyword)
            st.dataframe(results)
        else:
            st.error("Please enter a keyword.")

elif search_type == "By Person":
    person = st.sidebar.text_input("Enter person name")
    if st.sidebar.button("Search"):
        if person:
            results = movie_service.query_by_person(person)
            st.dataframe(results)
        else:
            st.error("Please enter a person name.")

elif search_type == "By Studio":
    studio = st.sidebar.text_input("Enter studio name")
    if st.sidebar.button("Search"):
        if studio:
            results = movie_service.query_by_studio(studio)
            st.dataframe(results)
        else:
            st.error("Please enter a studio name.")

# Additional section to show movie details if results are available
if 'results' in locals() and not results.empty:
    st.header("Movie Details")
    movie_details = movie_service.get_movie_details(results)
    st.dataframe(movie_details)

