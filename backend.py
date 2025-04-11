import streamlit as st
from game_recommender import GameRecommender
import pandas as pd
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import os
from google.cloud import storage
from google.oauth2 import service_account

# Initialize GCS client with error handling
def init_gcs_client():
    try:
        secrets = st.secrets["gcp_service_account"]
        credentials = service_account.Credentials.from_service_account_info(secrets)
        return storage.Client(credentials=credentials)
    except Exception as e:
        st.error(f"Failed to initialize GCS client: {str(e)}")
        return None

# Initialize client (do this once at app startup)
client = init_gcs_client()
bucket_name = "recommender-ak27"  # Your bucket name

def download_model_from_gcs(blob_name, local_path=None):
    """Downloads a file from GCS to local storage."""
    if not client:
        return None
        
    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        if not blob.exists():
            st.error(f"Model file {blob_name} not found in GCS")
            return None
            
        if not local_path:
            local_path = os.path.join("models", os.path.basename(blob_name))
            
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        blob.download_to_filename(local_path)
        return local_path
    except Exception as e:
        st.error(f"Failed to download model: {str(e)}")
        return None

@st.cache_resource
def load_models_and_data():
    """Load all necessary models and data files"""
    # Download files from GCS if needed
    required_files = {
        'knn_model': 'models/game_recommender_knn_model.pkl',
        'cosine_matrix': 'models/cosine_sim_matrix.pkl',
        'processed_data': 'models/game_data_processed.pkl',
        'game_names': 'models/game_names.pkl',
        'scaler': 'models/minmax_scaler.pkl',
        'one_hot_columns': 'models/one_hot_columns.pkl'
    }
    
    # Download files from GCS
    local_paths = {}
    for name, remote_path in required_files.items():
        local_path = download_model_from_gcs(remote_path)
        if not local_path:
            st.error(f"Failed to download {name} from GCS")
            return None
        local_paths[name] = local_path
    
    # Load all components
    try:
        # Load recommender models
        knn_rec = GameRecommender(model_type='knn')
        knn_rec.load(
            model_path=local_paths['knn_model'],
            data_path=local_paths['processed_data']
        )

        cosine_rec = GameRecommender(model_type='cosine')
        cosine_rec.load(
            model_path=local_paths['knn_model'],  # KNN model still needed for data alignment
            data_path=local_paths['processed_data'],
            similarity_matrix_path=local_paths['cosine_matrix']
        )
        
        # Load additional components
        scaler = joblib.load(local_paths['scaler'])
        one_hot_columns = joblib.load(local_paths['one_hot_columns'])
        game_names = joblib.load(local_paths['game_names'])
        
        # Load complete game data
        complete_game_data = pd.read_csv('data/games.csv')
        
        return {
            'knn_recommender': knn_rec,
            'cosine_recommender': cosine_rec,
            'scaler': scaler,
            'one_hot_columns': one_hot_columns,
            'game_names': game_names,
            'complete_game_data': complete_game_data
        }
        
    except Exception as e:
        st.error(f"Failed to load models: {str(e)}")
        return None

# Load all data and models
data_models = load_models_and_data()
if not data_models:
    st.error("Failed to initialize application. Please check the logs.")
    st.stop()

# Assign to variables for easier access
knn_recommender = data_models['knn_recommender']
cosine_recommender = data_models['cosine_recommender']
scaler = data_models['scaler']
one_hot_columns = data_models['one_hot_columns']
complete_game_data = data_models['complete_game_data']
game_names = data_models['game_names']

def preprocess_user_input(user_input):
    """Preprocess user input to match training data format"""
    # Create DataFrame from user input
    df = pd.DataFrame([user_input])
    
    # Convert year to string (categorical)
    df['Year_of_Release'] = df['Year_of_Release'].astype(str)
    
    # Select all columns with datatype object
    column_object = df.select_dtypes(include=['object']).columns
    
    # Convert categorical data to one-hot encoding
    one_hot_user = pd.get_dummies(df[column_object])
    
    # Create a DataFrame with all expected one-hot columns initialized to 0
    expected_one_hot = pd.DataFrame(0, index=[0], columns=one_hot_columns)
    
    # Update with actual values from one_hot_user
    for col in one_hot_user.columns:
        if col in expected_one_hot.columns:
            expected_one_hot[col] = one_hot_user[col]
    
    # Drop original categorical columns
    df.drop(column_object, axis=1, inplace=True)
    
    # Scale numerical columns
    numerical_cols = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'User_Score']
    df[numerical_cols] = scaler.transform(df[numerical_cols])
    
    # Combine numerical and one-hot encoded data
    processed_data = pd.concat([df, expected_one_hot], axis=1)
    
    return processed_data.values[0]  # Return as numpy array
# First, add this at the top with your other imports
import pandas as pd

# Load the complete game data (add this where you load your other data)
@st.cache_data
def load_game_data():
    return pd.read_csv('data/games.csv')

complete_game_data = load_game_data()

# Then modify your display_recommendations function:
def display_recommendations(recommendations,name):
    """Display recommendations with dataframe, visualizations, and complete details"""
    rec_df = pd.DataFrame(recommendations, columns=['Game', 'Score'])
    rec_df['Rank'] = range(1, len(rec_df)+1)
        
    # Display as an interactive dataframe
    st.dataframe(
        rec_df[['Rank', 'Game', 'Score']].set_index('Rank'),
        use_container_width=True,
        column_config={
            "Game": st.column_config.TextColumn("Game Title", width="large"),
            "Score": st.column_config.NumberColumn(
                "Similarity Score",
                format="%.4f",
                width="medium",
                help="Higher scores indicate better matches"
            )
        }
    )
    
    # Visualization
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Recommendation Scores")
        fig = px.bar(
            rec_df,
            x='Game',
            y='Score',
            color='Score',
            color_continuous_scale='blues',
            text='Score',
            labels={'Score': 'Similarity Score', 'Game': 'Recommended Game'}
        )
        fig.update_traces(
            texttemplate='%{text:.3f}', 
            textposition='outside',
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5
        )
        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Similarity Score",
            yaxis_range=[0, 1.1 if rec_df['Score'].max() <= 1 else None],
            showlegend=False,
            hovermode="x"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Score Distribution")
        fig2 = px.pie(
            rec_df,
            names='Game',
            values='Score',
            hole=0.3,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig2.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Score: %{value:.3f}"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Add expander with complete game details
    with st.expander("View Complete Game Details", expanded=True):
        # Filter the complete game data for our recommendations
        recommended_games = rec_df['Game'].tolist()
        game_details = complete_game_data[complete_game_data['Name'].isin(recommended_games)]
        
        if not game_details.empty:
            # Display the complete data with nice formatting
            st.dataframe(
                game_details,
                use_container_width=True,
                column_config={
                    "Name": st.column_config.TextColumn("Game Title", width="large"),
                    "Platform": st.column_config.TextColumn("Platform"),
                    "Year_of_Release": st.column_config.NumberColumn("Year", format="%d"),
                    "Genre": st.column_config.TextColumn("Genre"),
                    "Publisher": st.column_config.TextColumn("Publisher"),
                    "NA_Sales": st.column_config.NumberColumn("NA Sales (M)", format="%.2f"),
                    "EU_Sales": st.column_config.NumberColumn("EU Sales (M)", format="%.2f"),
                    "JP_Sales": st.column_config.NumberColumn("JP Sales (M)", format="%.2f"),
                    "Global_Sales": st.column_config.NumberColumn("Global Sales (M)", format="%.2f"),
                    "Critic_Score": st.column_config.NumberColumn("Critic Score", format="%d"),
                    "User_Score": st.column_config.NumberColumn("User Score", format="%.1f"),
                    "Rating": st.column_config.TextColumn("Rating")
                }
            )
            
            # Add download button
            csv = game_details.to_csv(index=False).encode('utf-8')
            col1,col2,col3,co4,col5=st.columns([1,1,2,1,1])
            col3.download_button(label=f"Download {name} recommendations CSV",data=csv,file_name=f'{name}_recommendations.csv',mime='text/csv',key='download_full_details',use_container_width=True,on_click="ignore")
        else:
            st.warning("Could not find complete details for all recommended games")

class GameRecommender:
    def __init__(self, model_type='knn'):
        self.model_type = model_type
        self.model = None
        self.data = None
        self.game_names = None
        self.similarity_matrix = None

    def load(self, model_path, data_path, similarity_matrix_path=None):
        self.model = joblib.load(model_path)
        self.data = joblib.load(data_path)
        self.game_names = self.data.index.tolist()

        if self.model_type == 'cosine' and similarity_matrix_path:
            self.similarity_matrix = joblib.load(similarity_matrix_path)

    def recommend(self, game_name, n_recommendations=5):
        if game_name not in self.game_names:
            raise ValueError("Game not found in the dataset.")

        game_idx = self.game_names.index(game_name)

        if self.model_type == 'knn':
            distances, indices = self.model.kneighbors(
                [self.data.iloc[game_idx].values],
                n_neighbors=n_recommendations + 1
            )
            recommendations = [(self.game_names[i], round(d, 4)) for i, d in zip(indices[0][1:], distances[0][1:])]

        elif self.model_type == 'cosine':
            sim_scores = list(enumerate(self.similarity_matrix[game_idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n_recommendations + 1]
            recommendations = [(self.game_names[i], round(score, 4)) for i, score in sim_scores]

        else:
            raise ValueError("Invalid model type.")

        return recommendations