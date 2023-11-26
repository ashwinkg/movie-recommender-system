import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=7c4fa270692549812ce1dcf190d6258c&language=en-US".format(
        movie_id)
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(input_movie):
    index = movies[movies['title'] == input_movie].index[0]
    distances = similarity[index]
    sorted_movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for movie in sorted_movie_list:
        movie_id = movies.iloc[movie[0]].movie_id
        recommended_movies.append(movies.iloc[movie[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Recommend'):
    recommended_movie_list, recommended_movie_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_list[0])
        st.image(recommended_movie_poster[0])
    with col2:
        st.text(recommended_movie_list[1])
        st.image(recommended_movie_poster[1])

    with col3:
        st.text(recommended_movie_list[2])
        st.image(recommended_movie_poster[2])
    with col4:
        st.text(recommended_movie_list[3])
        st.image(recommended_movie_poster[3])
    with col5:
        st.text(recommended_movie_list[4])
        st.image(recommended_movie_poster[4])
