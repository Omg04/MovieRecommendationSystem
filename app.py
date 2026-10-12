import streamlit as st
import pickle
import joblib

movies_df = pickle.load(open('movies.pkl', 'rb')).reset_index(drop=True)
try:
    similarity = joblib.load('similarity.pkl')
except Exception:
    similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies_df['title'].values

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    recommended_movie = []
    for i in movie_list:
        recommended_movie.append(movies_df.iloc[i[0]].title)
    return recommended_movie

st.title('Movie Recommendation System')
selected_movie = st.selectbox('Select a movie:', movies_list)

if st.button('Recommend'):
    recommendations = recommend(selected_movie)
    for i in recommendations:
        st.write(i)