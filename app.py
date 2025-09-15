import pickle
import pandas as pd
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import quote_plus
from io import BytesIO

if not (os.path.exists("movie_dict.pkl") and os.path.exists("similarity.pkl")):
    print("🔄 Building dataset from CSV...")

    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")

    # Merge datasets
    movies = movies.merge(credits, on='title')

    # Feature engineering (you can customize)
    movies['overview'] = movies['overview'].fillna('')
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['overview']).toarray()

    # Compute similarity
    similarity = cosine_similarity(vectors)

    # Save pickle files
    pickle.dump(movies.to_dict(), open("movie_dict.pkl", "wb"))
    pickle.dump(similarity, open("similarity.pkl", "wb"))

else:
    print("✅ Loading existing pickle files")
    movies = pd.DataFrame(pickle.load(open("movie_dict.pkl", "rb")))
    similarity = pickle.load(open("similarity.pkl", "rb"))

TMDB_KEY = "66774302c212b13b133cfef8e9206d83"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=0.6,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=frozenset(["GET", "HEAD"])
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)
session.headers.update({"User-Agent": "movie-recommender/1.0"})

@st.cache_data(show_spinner=False)
def fetch_poster_bytes(movie_id: int, title: str | None = None):
    try:
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_KEY}&language=en-US"
        r = session.get(details_url, timeout=10)
        r.raise_for_status()
        data = r.json()
        poster_path = data.get("poster_path")
        if poster_path:
            img_url = IMAGE_BASE + poster_path
            img_resp = session.get(img_url, timeout=10)
            if img_resp.status_code == 200 and img_resp.headers.get("Content-Type", "").startswith("image"):
                return img_resp.content
    except:
        pass

    if title:
        try:
            q = quote_plus(title)
            search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_KEY}&query={q}&language=en-US&page=1&include_adult=false"
            r = session.get(search_url, timeout=10)
            r.raise_for_status()
            results = r.json().get("results", [])
            if results:
                poster_path = results[0].get("poster_path")
                if poster_path:
                    img_url = IMAGE_BASE + poster_path
                    img_resp = session.get(img_url, timeout=10)
                    if img_resp.status_code == 200 and img_resp.headers.get("Content-Type", "").startswith("image"):
                        return img_resp.content
        except:
            pass

    return None

def recommend(movie_title, n=10):
    idx = movies[movies['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    names, poster_bytes_list, ids = [], [], []
    for pair in distances[1:n+1]:
        i = pair[0]
        row = movies.iloc[i]
        mid = row.get('movie_id')
        title = row.get('title')
        names.append(title)
        ids.append(mid)
        bytes_img = None
        if pd.notna(mid):
            try:
                bytes_img = fetch_poster_bytes(int(mid), title=title)
            except:
                pass
        poster_bytes_list.append(bytes_img)
    return names, poster_bytes_list, ids

st.set_page_config(layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .movie-card {
        text-align: center;
        padding: 10px;
        border-radius: 12px;
        background: #1e1e2f;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
    }
    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0px 4px 20px rgba(255, 255, 255, 0.2);
    }
    .movie-title {
        font-size: 15px;
        font-weight: bold;
        margin-top: 8px;
        color: #f5f5f5;
    }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px 20px;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #e60000;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 style='text-align: center; color: #ffcc00;'>🍿 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Discover top movies you'll love, based on your favorites 🎬</p>", unsafe_allow_html=True)

movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

if 'movie_id' not in movies.columns:
    st.error("movie_id column is missing from movie_dict.pkl.")
    st.stop()

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Choose a movie:", movie_list)

if st.button("✨ Show Recommendations"):
    names, posters, mids = recommend(selected_movie, n=10)

    for row in range(0, 10, 5):  # 2 rows, 5 per row
        cols = st.columns(5)
        for name, poster_bytes, col, mid in zip(names[row:row+5], posters[row:row+5], cols, mids[row:row+5]):
            with col:
                st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                if poster_bytes:
                    st.image(BytesIO(poster_bytes), use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/500x750?text=No+Image", use_container_width=True)
                st.markdown(f"<div class='movie-title'>{name}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
