import os
import pickle
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the TMDB API key from environment variables
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Load the processed data and similarity matrix
def load_data():
    with open('movie_data.pkl', 'rb') as file:
        movies, cosine_sim = pickle.load(file)
    return movies, cosine_sim

# Function to get movie recommendations
def get_recommendations(title, cosine_sim):
    movies, _ = load_data()
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

# Function to fetch movie poster URL from TMDB
def fetch_poster(movie_id):
    if not TMDB_API_KEY:
        raise ValueError("TMDB API key is not set.")
    
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_path
    else:
        raise ValueError("Poster not found for the movie.")
