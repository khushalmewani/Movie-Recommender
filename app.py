import streamlit as st
import os
from dotenv import load_dotenv
from movie_recommend import get_recommendations, fetch_poster, load_data  # Import load_data
from poster_generation import generate_movie_poster

# Load environment variables from .env file
load_dotenv()

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

# --------- HOME PAGE ---------
def home():
    st.markdown(""" 
        <style>
            .main {
                background: linear-gradient(to right, #1c92d2, #f2fcfe);
            }
            .box {
                background-color: #ffffffcc;
                padding: 50px;
                border-radius: 20px;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                transition: 0.3s ease;
            }
            .box:hover {
                transform: scale(1.05);
                background-color: #ffffffee;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>🎥 Movie Assistant</h1>", unsafe_allow_html=True)
    st.markdown("##")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎬 Movie Recommendation", use_container_width=True):
            st.session_state.page = "recommendation"
            st.rerun()
        st.markdown('<div class="box">Find movies like your favorites</div>', unsafe_allow_html=True)

    with col2:
        if st.button("🖼️ Poster Generator", use_container_width=True):
            st.session_state.page = "poster"
            st.rerun()
        st.markdown('<div class="box">Generate custom movie posters</div>', unsafe_allow_html=True)

# --------- MOVIE RECOMMENDATION PAGE ---------
def recommendation_page():
    st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommendation</h1>", unsafe_allow_html=True)

    # Load movie data and recommendations
    movies, cosine_sim = load_data()  # This line now works because load_data is imported from movie_recommend.py

    selected_movie = st.selectbox("Select a movie:", movies['title'].values)
    
    if st.button('Recommend', key='recommend_button'):
        recommendations = get_recommendations(selected_movie, cosine_sim)
        st.write("Top 10 recommended movies:")
        
        # Create a 2x5 grid layout
        for i in range(0, 10, 5):  # Loop over rows (2 rows, 5 movies each)
            cols = st.columns(5)  # Create 5 columns for each row
            for col, j in zip(cols, range(i, i+5)):
                if j < len(recommendations):
                    movie_title = recommendations.iloc[j]['title']
                    movie_id = recommendations.iloc[j]['movie_id']
                    poster_url = fetch_poster(movie_id)
                    with col:
                        st.image(poster_url, width=130)
                        st.write(movie_title)

    # Back button
    st.markdown("<div style='text-align: right; margin-top: 50px;'>", unsafe_allow_html=True)
    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --------- POSTER GENERATION PAGE ---------
def poster_page():
    st.markdown("<h1 style='text-align: center;'>🖼️ Poster Generator</h1>", unsafe_allow_html=True)

    # Input fields for movie details
    movie_name = st.text_input("Enter the movie name:")
    
    # Dropdown for selecting genre
    genres = [
        "Action", "Adventure", "Animation", "Comedy", "Crime", 
        "Documentary", "Drama", "Fantasy", "Horror", "Musical",
        "Mystery", "Romance", "Sci-Fi", "Thriller", "Western"
    ]
    selected_genre = st.selectbox("Select movie genre:", genres)
    
    # Generate button
    if st.button("Generate Poster", key='generate_poster_button'):
        if movie_name:
            with st.spinner("Generating your movie poster..."):
                # Generate the poster
                try:
                    poster_image = generate_movie_poster(movie_name, selected_genre)
                    st.success("Poster generated successfully!")
                    st.image(poster_image, caption=f"{movie_name} - {selected_genre}", use_column_width=True)
                except Exception as e:
                    st.error(f"Failed to generate poster: {str(e)}")
        else:
            st.warning("Please enter a movie name.")
    
    # Back button
    st.markdown("<div style='text-align: right; margin-top: 50px;'>", unsafe_allow_html=True)
    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --------- PAGE ROUTING ---------
if st.session_state.page == "home":
    home()
elif st.session_state.page == "recommendation":
    recommendation_page()
elif st.session_state.page == "poster":
    poster_page()
