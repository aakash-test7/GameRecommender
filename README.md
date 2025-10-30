# Game Recommendation System 🎮

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
                
A content-based game recommendation system that suggests similar games based on either:
- An existing game in the database
- Custom game features provided by the user

🔗 **Live Demo:** [Game Recommendations](https://aakash-game.streamlit.app/)  

https://github.com/user-attachments/assets/e07e6f04-0721-4333-86f1-ade5016da9eb

## Features ✨

- **Dual Recommendation Methods**:
  - KNN (Euclidean distance)
  - Cosine Similarity
- **Interactive Visualizations**:
  - Bar charts showing similarity scores
  - Pie charts showing score distributions
- **Complete Game Details**:
  - View all metadata for recommended games
  - Download recommendations as CSV
- **Cloud Integration**:
  - Models stored on Google Cloud Storage
  - Automatic download and caching
- **Responsive UI**:
  - Clean, modern interface
  - Mobile-friendly design

## Project Structure 📂

```
game-recommender/
├── data/
│   └── games.csv               # Complete game dataset
├── models/                     # (Auto-created)
│   ├── game_data_processed.pkl # Processed game data
│   ├── game_names.pkl          # List of game names
│   ├── cosine_sim_matrix.pkl   # Cosine similarity matrix
│   ├── game_recommender_knn_model.pkl  # KNN model
│   ├── minmax_scaler.pkl       # Feature scaler
│   └── one_hot_columns.pkl     # One-hot encoded columns
├── .streamlit/
│   ├── config.toml             # Streamlit configuration
│   └── secrets.toml            # GCP credentials (ignored in git)
├── app.py                      # Main Streamlit application
├── backend.py                  # Important functions and connectors
├── game_recommender.py         # Recommendation engine
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation 🛠️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aakash-test7/GameRecommender.git
   cd game-recommender
   ```

2. **Set up Python environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure GCP credentials**:
   - Create `secrets.toml` in `.streamlit/` with your service account info:
     ```toml
     [gcp_service_account]
     type = "service_account"
     project_id = "your-project-id"
     private_key_id = "your-key-id"
     private_key = "-----BEGIN PRIVATE KEY-----..."
     client_email = "your-service-account@your-project.iam.gserviceaccount.com"
     client_id = "your-client-id"
     auth_uri = "https://accounts.google.com/o/oauth2/auth"
     token_uri = "https://oauth2.googleapis.com/token"
     auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
     client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
     ```

4. **Prepare data files**:
   - Place `games.csv` in the `data/` directory
   - Ensure model files are in your GCS bucket `recommender-27`

## Usage 🚀

1. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Using the recommender**:
   - *Game-based recommendations*:
     1. Select "Recommend by Game"
     2. Choose a game from the dropdown
     3. Select recommendation method
     4. Get recommendations
   
   - *Feature-based recommendations*:
     1. Select "Recommend by Features"
     2. Fill in the game attributes
     3. Select recommendation method
     4. Get personalized recommendations

## Configuration ⚙️

Customize the app by modifying `.streamlit/config.toml`:
```toml
[theme]
base = "light"
primaryColor = "#4b9cd3"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#31333f"
```

## Technical Details 🔧

- **Data Processing**:
  - Numerical features scaled using MinMaxScaler
  - Categorical features one-hot encoded
  - Missing values handled during preprocessing

- **Recommendation Algorithms**:
  - **KNN**: Finds nearest neighbors in feature space
  - **Cosine Similarity**: Measures angle between game vectors

- **Performance**:
  - Models cached using Streamlit's caching mechanisms
  - GCS downloads only occur when models are updated

## Troubleshooting 🐛

**Issue**: "Failed to initialize GCS client"
- Verify `secrets.toml` contains valid credentials
- Ensure the service account has Storage Object Viewer permissions

**Issue**: "Model files not found"
- Check files exist in GCS bucket
- Verify bucket name in `app.py` matches your GCS bucket

**Issue**: Visualizations not loading
- Ensure all Plotly dependencies are installed
- Check browser console for JavaScript errors

## Future Enhancements 🚧

- [ ] Collaborative filtering hybrid approach
- [ ] Dark mode toggle
- [ ] Social sharing of recommendations

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Happy gaming!** 🎮 If you have any questions, [@Aakash](https://github.com/aakash-test7)
