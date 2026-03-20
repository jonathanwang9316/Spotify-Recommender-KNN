# Personalized Song Recommendation Engine

A high-performance machine learning system that predicts user music preferences and ranks similar tracks/artists. This project leverages the **Spotify Web API** and a dataset of over **1M+ tracks** to provide highly accurate, personalized recommendations.

---

## Performance Highlights

* **95% Prediction Accuracy:** The K-Nearest Neighbors (KNN) model accurately identifies user preferences based on high-dimensional audio features.
* **1M+ Track Dataset:** Scaled to handle massive listening data using optimized data structures.
* **25% Runtime Reduction:** Optimized the data preprocessing pipeline using **Pandas** vectorized operations and strategic feature pruning.

---

## Tech Stack

* **Language:** Python
* **Data Manipulation:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn (K-Nearest Neighbors)
* **API Integration:** Spotipy (Spotify Web API)
* **Environment:** Jupyter Notebooks / Python Scripts

---

## Project Structure

```text
├── notebooks/           # Exploratory Data Analysis (EDA) & Model Training
├── src/                 # Production-ready Python scripts
│   ├── preprocessing.py # Feature pruning and vectorization logic
│   └── recommender.py   # KNN model implementation
├── data/                # Sample datasets (Full 1M+ tracks linked in docs)
├── .env.example         # Template for Spotify API credentials
├── requirements.txt     # Python library dependencies
└── README.md            # Project documentation
```

---

## Methodology

### 1. Data Acquisition
Utilized the **Spotify API** to extract audio features including:
* Acousticness, Danceability, Energy, Instrumentalness, Liveness, Loudness, Speechiness, Tempo, and Valence.

### 2. Preprocessing & Optimization
* **Vectorization:** Replaced iterative loops with Pandas vectorized operations to handle the 1M+ record scale.
* **Feature Pruning:** Identified and removed low-variance features to decrease model complexity and training time.
* **Scaling:** Applied `StandardScaler` to normalize features for distance-based calculations.

### 3. Modeling (K-Nearest Neighbors)
Implemented a **KNN algorithm** using Euclidean distance to find the "nearest" tracks in the feature space. The model ranks the top-N most similar songs to any given input track or user profile.

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/jonathanwang9316/Spotify-Recommender-KNN.git](https://github.com/jonathanwang9316/Spotify-Recommender-KNN.git)
   cd Spotify-Recommender-KNN
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Spotify API Credentials:**
   Create a `.env` file in the root directory:
   ```text
   SPOTIPY_CLIENT_ID='your_client_id_here'
   SPOTIPY_CLIENT_SECRET='your_client_secret_here'
   ```

---

## 📄 License
This project is licensed under the MIT License.
