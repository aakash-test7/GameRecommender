### **Game Recommendation System Pipeline Summary**

#### **1. Data Collection & Preparation**
- **Source**: Kaggle dataset (`video-game-sales-with-ratings`)
- **Preprocessing Steps**:
  - Dropped irrelevant columns (`Global_Sales`, `Critic_Score`, etc.)
  - Handled missing values (dropped rows with NaN in key columns)
  - Filtered rare platforms (<350 entries) and the `Misc` genre
  - Converted categorical features (`Year_of_Release`) to strings
  - Removed invalid `User_Score` entries (e.g., "tbd") and converted to float
  - Dropped high-cardinality columns (`Developer`)

#### **2. Feature Engineering**
- **One-Hot Encoding**: Applied to categorical columns (`Platform`, `Genre`, etc.)
- **Numerical Scaling**: MinMaxScaler for sales metrics and user scores
- **Final Features**: 320 dimensions (numeric + one-hot encoded)

#### **3. Model Building**
- **Algorithms**:
  1. **KNN (Euclidean Distance)**
     - `NearestNeighbors(metric='euclidean')`
     - Recommends games based on feature-space proximity
  2. **Cosine Similarity**
     - Measures angle between game vectors in feature space
     - Captures directional similarity rather than magnitude

#### **4. Evaluation Metrics**
- **Calinski-Harabasz Score**: Higher = better cluster separation
- **Davies-Bouldin Score**: Lower = better cluster compactness

#### **5. Deployment Pipeline**
- **Model Persistence**:
  - Saved as `.pkl` files:
    - KNN model
    - Cosine similarity matrix
    - Scaler
    - Processed game data
    - Game names
    - One-hot encoded columns
- **Cloud Integration**:
  - Models stored in Google Cloud Storage (GCS)
  - Signed URLs for secure access
  - Automatic caching via Streamlit

#### **6. Streamlit App Features**
- **Two Recommendation Modes**:
  1. **Game-Based**: Select from existing titles
  2. **Feature-Based**: Input custom game attributes
- **Output**:
  - Interactive tables with similarity scores
  - Visualizations (bar/pie charts)
  - Raw game details in expandable sections
  - CSV download option

#### **7. Key Files**
```
├── app.py                      # Main application logic
├── backend.py                  # Recommendation engine class
├── data/games.csv              # Raw game metadata
├── models/                     # Serialized artifacts
│   ├── *.pkl                   # Models, data, and scalers
└── .streamlit/
    ├── config.toml             # UI/theme config
    └── secrets.toml            # GCP credentials
```

#### **8. Performance Notes**
- **Input Shape**: `(n_samples, 320)` features
- **Cold Start**: Downloads models from GCS on first run
- **Caching**: Uses Streamlit’s `@cache_resource` for efficiency

---

### **Pipeline Diagram**
```
[Data Collection] → [Cleaning] → [Feature Engineering] → [Model Training]
       ↓                                      ↓
[GCS Storage] ← [Serialization] ← [Evaluation]
       ↓
[Streamlit UI] → [Recommendations]
```

This pipeline balances accuracy (via dual-algorithm support) and usability (intuitive UI with visualizations). The modular design allows easy updates to models/data.