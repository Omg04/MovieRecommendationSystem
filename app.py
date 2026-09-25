import ast
import pickle
from pathlib import Path

import pandas as pd
import streamlit as st
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

base_dir = Path(__file__).resolve().parent
movies_path = base_dir / 'movies.pkl'
similarity_path = base_dir / 'similarity.pkl'


def convert(obj):
    return [item['name'] for item in ast.literal_eval(obj)]


def convert_keywords(obj):
    items = ast.literal_eval(obj)
    return [item['name'] for item in items[:3]]


def convert_crew(obj):
    for item in ast.literal_eval(obj):
        if item.get('job') == 'Director':
            return [item.get('name')]
    return []


def build_model_files():
    movies = pd.read_csv(base_dir / 'tmdb_5000_movies.csv')
    credits = pd.read_csv(base_dir / 'tmdb_5000_credits.csv')
    movies = movies.merge(credits, on='title')
    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies = movies.dropna().drop_duplicates()

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['crew'] = movies['crew'].apply(convert_crew)
    movies['cast'] = movies['cast'].apply(convert_keywords)
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    for column in ['genres', 'keywords', 'crew', 'cast']:
        movies[column] = movies[column].apply(lambda x: [item.replace(' ', '') for item in x])

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    movies_df = movies[['movie_id', 'title', 'tags']].copy()
    movies_df['tags'] = movies_df['tags'].apply(lambda x: ' '.join(x))
    movies_df['tags'] = movies_df['tags'].apply(lambda x: x.lower())

    ps = PorterStemmer()
    movies_df['tags'] = movies_df['tags'].apply(lambda x: ' '.join(ps.stem(word) for word in x.split()))

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies_df['tags']).toarray()
    similarity = cosine_similarity(vectors)

    with movies_path.open('wb') as movies_file:
        pickle.dump(movies_df, movies_file)
    with similarity_path.open('wb') as similarity_file:
        pickle.dump(similarity, similarity_file)

    return movies_df, similarity


if not movies_path.exists() or not similarity_path.exists():
    build_model_files()

with movies_path.open('rb') as movies_file:
    movies_df = pickle.load(movies_file)
with similarity_path.open('rb') as similarity_file:
    similarity = pickle.load(similarity_file)

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
selected_movie = st.selectbox('Select a movie', movies_list)

if st.button('Recommend'):
    recommendations = recommend(selected_movie)
    for i in recommendations:
        st.write(i)