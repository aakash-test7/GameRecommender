import joblib
from sklearn.metrics.pairwise import cosine_similarity
import io

class GameRecommender:
    def __init__(self, model_type='knn'):
        self.model_type = model_type
        self.model = None
        self.data = None
        self.game_names = None
        self.similarity_matrix = None

    def load_from_gcs(self, storage_client, bucket_name, model_path, data_path, similarity_matrix_path=None):
        """Load models and data directly from GCS bucket"""
        bucket = storage_client.bucket(bucket_name)
        
        # Load model
        model_blob = bucket.blob(model_path)
        self.model = joblib.load(io.BytesIO(model_blob.download_as_bytes()))
        
        # Load data
        data_blob = bucket.blob(data_path)
        self.data = joblib.load(io.BytesIO(data_blob.download_as_bytes()))
        self.game_names = self.data.index.tolist()

        if self.model_type == 'cosine' and similarity_matrix_path:
            # Load similarity matrix
            sim_blob = bucket.blob(similarity_matrix_path)
            self.similarity_matrix = joblib.load(io.BytesIO(sim_blob.download_as_bytes()))

    def load_from_bytes(self, model_bytes, data_bytes, similarity_matrix_bytes=None):
        """Load models and data from bytes objects"""
        self.model = joblib.load(io.BytesIO(model_bytes))
        self.data = joblib.load(io.BytesIO(data_bytes))
        self.game_names = self.data.index.tolist()

        if self.model_type == 'cosine' and similarity_matrix_bytes:
            self.similarity_matrix = joblib.load(io.BytesIO(similarity_matrix_bytes))

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
