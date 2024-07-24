import streamlit as st
import pandas as pd
import requests

def get_simMat():
    import pickle
    
    file_prefix = 'sim_mat_tfIdf_part_'
    merged_data = bytearray()

    for x in range(4):
        part_file = f"{file_prefix}{x:02}"
        
        with open(part_file, "rb") as file:
            merged_data.extend(file.read())
    
    matrix = pickle.loads(merged_data)
    return matrix

movies = pd.read_pickle('movies.pkl')
#SIM_MAT1 = "sim_mat_tfIdf.pkl" #vectorization technique used: TF IDF (TfidfVectorizer())
#SIM_MAT2 = "sim_mat_bow.pkl" #vectorization technique used: Bag of Words (CountVectorizer())
SIM_MAT = get_simMat()


movie_options = [
    f"{row['title']} ({row['year']})" for _,row in movies.iterrows()
]

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=4b388263db5d0307369cd202fc7be6ed&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = SIM_MAT[movie_index]
    rec_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6] #top 5 recommendation

    recommended_movies, rec_movie_posters = [], []
    for x in rec_movies_list:
        rec_movie_posters.append(fetch_poster(movies.iloc[x[0]].id)) #fetch poster from API
        recommended_movies.append(f'{movies.iloc[x[0]].title} ({movies.iloc[x[0]].year})')
    
    return recommended_movies, rec_movie_posters

st.title('Movie Recommendation System')

selected_movie = st.selectbox(
    'Enter a movie you liked',
    options = movie_options
)

selected_movie = " ".join(selected_movie.split()[:-1])

if st.button('Recommend'):
    rec_movie, mov_poster = recommend(selected_movie)
    
    #CSS for responsive image and text
    st.markdown("""
    <style>
        .movie-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            margin: 10px;
            padding: 5px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        .movie-card img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }
        .movie-card-title {
            font-size: 14px;
            font-weight: bold;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    for x, col in enumerate([col1,col2,col3,col4,col5]):
        with col:
            st.markdown(f"""
            <div class="movie-card">
                <a href="{mov_poster[x]}"> <img src="{mov_poster[x]}" alt="{rec_movie[x]}"> </a>
                <div class="movie-card-title">{rec_movie[x]}</div>
            </div>
            """, unsafe_allow_html=True)