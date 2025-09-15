# 🎬 Movie Recommender System

An interactive **Movie Recommendation System** built with [Streamlit](https://streamlit.io/) and [TMDb API](https://www.themoviedb.org/documentation/api).  
It suggests movies similar to the one you select, showing posters, titles, and making the UI engaging and easy to use.  

---

## 🚀 Features
- Suggests **10 similar movies** based on the selected title.  
- Fetches real-time movie posters using **TMDb API**.  
- Clean, responsive, and immersive **Streamlit UI**.  
- Caches results for faster performance.  
- Fallback image if no poster is found.  

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Then open the link provided in your terminal (default: `http://localhost:8501/`) in your browser.  

---

## ⚙️ Dataset
This project uses precomputed similarity scores and movie metadata stored in:
- `movie_dict.pkl`
- `similarity.pkl`

👉 These files are **ignored via `.gitignore`** (not uploaded to GitHub).  
Please generate or download them separately before running the app.  

---

## 🔑 API Key
You need a [TMDb API key](https://developers.themoviedb.org/3/getting-started/introduction).  
Replace the placeholder in `app.py`:

```python
TMDB_KEY = "your_api_key_here"
```

---

## 📂 Project Structure

```
.
├── app.py              # Main Streamlit app
├── movie_dict.pkl      # Movie metadata (ignored in git)
├── similarity.pkl      # Similarity matrix (ignored in git)
├── requirements.txt    # Dependencies
├── .gitignore          # Ignore datasets and cache files
└── README.md           # Project documentation
```

---

## 🖼️ Demo

<img width="1919" height="1017" alt="image" src="https://github.com/user-attachments/assets/56649579-9642-469c-8ebc-f71388f68fa9" />
  
<img width="1886" height="1001" alt="image" src="https://github.com/user-attachments/assets/dc7c0164-5af0-4122-b25a-0ed3f2964592" />

---

## 🤝 Contributing
Pull requests are welcome!  
If you’d like to improve recommendations, UI, or add features, feel free to fork the repo and submit a PR.  

---


## 🚀 Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/movie-recommender.git
   cd movie-recommender
   ```

2. **Create a virtual environment (recommended)**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Linux/Mac
   .venv\Scripts\activate    # On Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**  
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**  
   Once running, Streamlit will show a local URL (usually http://localhost:8501).  
   Open it in your browser to use the recommender system.


## 📜 License
This project is licensed under the **MIT License** – feel free to use and modify.  

---

⭐ If you like this project, don’t forget to **star the repo**!
