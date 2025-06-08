import pickle
import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")


# --- Function to fetch poster using TMDB API ---
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=463197e12777cc335131458a721a5afb&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    full_path = "https://image.tmdb.org/t/p/w500" + poster_path
    return full_path


# --- Function to recommend movies ---
def recommend(movie_name):
    index = movies[movies['title'] == movie_name].index[0]
    similar_movies = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)

    recommended_names = []
    recommended_posters = []

    for i in similar_movies[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_names.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_names, recommended_posters


# --- Load Data ---
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# --- Movie Dropdown ---
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Select a movie to get recommendations:", movie_list)

# --- Recommendation Output ---
if st.button("🔍 Show Recommendations"):
    names, posters = recommend(selected_movie)
    st.markdown("## ✅ Top 5 Recommended Movies:")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)  # ✅ Updated line
            st.caption(names[i])

