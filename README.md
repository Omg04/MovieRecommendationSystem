# 🎬 Movie Recommendation System

A content-based movie recommendation web application built with Python and Streamlit. This app uses the TMDB 5000 Movie Dataset to suggest similar movies based on metadata like genres, keywords, cast, and crew.

## 🚀 Features

* **Content-Based Filtering:** Recommends movies by analyzing plot summaries, genres, cast, and crew similarities.
* **Interactive Web Interface:** Clean UI built using Streamlit for a smooth user experience.
* **Cloud Deployment Ready:** Includes configuration files (`render.yaml`, `Procfile`, `setup.sh`) for seamless deployment on platforms like Render or Heroku.

## 📁 Project Structure

```text
├── MovieRecommendationSystem.ipynb # Jupyter notebook for data preprocessing and model building
├── app.py                         # Main Streamlit web application
├── tmdb_5000_movies.csv           # Movie dataset (metadata)
├── tmdb_5000_credits.csv          # Credits dataset (cast & crew)
├── requirements.txt               # Required Python packages
├── render.yaml                    # Render deployment configuration
├── Procfile                       # Process file for cloud hosting
└── setup.sh                       # Streamlit configuration setup script

```

## 🛠️ Tech Stack

* **Language:** Python
* **Framework:** Streamlit
* **Data Processing & ML:** Pandas, NumPy, Scikit-learn, NLTK

## 💻 Local Installation & Setup

If you want to run this project locally on your machine, follow these steps:

1. **Clone the repository:**
```bash
git clone https://github.com/Omg04/MovieRecommendationSystem
cd MovieRecommendationSystem

```


2. **Install the dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the Streamlit app:**
```bash
streamlit run app.py

```

## 👤 Author

* **Omg04** - [GitHub Profile](https://github.com/Omg04)

---
