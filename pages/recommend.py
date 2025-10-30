import streamlit as st
from backend import *
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def recommend_page():
    st.title("🎮 Game Recommendation System")
    st.write("Get game recommendations based on your favorite title or custom game features!")

    if 'active_view' not in st.session_state:
        st.session_state.active_view = None  # 'game' or 'feature'

    # Button layout
    col1, col2, col3 = st.columns([2, 1, 2])
    game_btn = col1.button("Recommend by Game", icon=":material/smart_toy:", use_container_width=True)
    feature_btn = col3.button("Recommend by Features", icon=":material/view_list:", use_container_width=True)

    # Update session state based on button clicks
    if game_btn:
        st.session_state.active_view = 'game'
    if feature_btn:
        st.session_state.active_view = 'feature'

    # Create tabs for different recommendation methods
    #tab1, tab2 = st.tabs(["Recommend by Game", "Recommend by Features"])

    #with tab1:
    if st.session_state.active_view == 'game':
        con=st.container(border=True)
        with con:
            # Select game
            games_list = knn_recommender.game_names
            selected_game = st.selectbox("Select a game", sorted(games_list), key='game_select')

            # Select model
            model_choice = st.selectbox("Choose recommendation method", 
                                    ['KNN (Euclidean)', 'Cosine Similarity'], key='model_choice1')
            
            # Number of recommendations
            num_recs = st.slider("Number of recommendations", 1, 10, 5, key='num_recs1')
        
            # Show recommendations
            col1,col2,col3,col4,col5=st.columns([1,1,2,1,1])
        if col3.button("Recommend", key='recommend1',use_container_width=True,icon=":material/network_intelligence:"):
            with st.spinner("Finding recommendations..."):
                recommender = knn_recommender if "KNN" in model_choice else cosine_recommender
                try:
                    recommendations = recommender.recommend(selected_game, num_recs)
                    
                    # Display success message and DataFrame
                    st.toast("Recommendation processed",icon=":material/manufacturing:")
                    st.success("Here are your recommendations:")
                    
                    display_recommendations(recommendations,selected_game)
                        
                except ValueError as e:
                    st.error(str(e))
                    st.error("Please try a different game or check your input.")

    #with tab2:
    if st.session_state.active_view == 'feature':
        st.subheader("Enter Game Features")
        
        # Create input form for all features
        with st.form("game_features"):
            con=st.container(border=True)
            with con:
                name = st.text_input("Game Name", "Custom Game")

                col1, col2 = st.columns(2)
                
                with col1:
                    platform = st.selectbox("Platform", ['Wii', 'PS3', 'X360', 'PS2', 'DS', 'PS4', 'PS', 'XB', 'PSP', 'PC', '3DS'])
                    year = st.number_input("Year of Release", min_value=1980, max_value=2023, value=2010)
                    genre = st.selectbox("Genre", ['Action', 'Adventure', 'Fighting', 'Misc', 'Platform', 
                                                'Puzzle', 'Racing', 'Role-Playing', 'Shooter', 'Simulation', 
                                                'Sports', 'Strategy'])
                    user_score = st.number_input("User Score", min_value=0.0, max_value=10.0, value=7.5)
                    publisher = st.text_input("Publisher", "Custom Publisher")
                    
                with col2:
                    na_sales = st.number_input("NA Sales (millions)", min_value=0.0, value=1.0)
                    eu_sales = st.number_input("EU Sales (millions)", min_value=0.0, value=1.0)
                    jp_sales = st.number_input("JP Sales (millions)", min_value=0.0, value=1.0)
                    other_sales = st.number_input("Other Sales (millions)", min_value=0.0, value=0.5)
                    rating = st.selectbox("Rating", ['E', 'E10+', 'T', 'M', 'RP'])

            con=st.container(border=True)

            model_choice_custom = con.selectbox("Choose recommendation method", 
                                            ['KNN (Euclidean)', 'Cosine Similarity'], key='model_choice2')
            num_recs_custom = con.slider("Number of recommendations", 1, 10, 5, key='num_recs2')
            col1,col2,col3,col4,col5=st.columns([1,1,2,1,1])
            submitted = col3.form_submit_button("Get Recommendations",use_container_width=True,icon=":material/network_intelligence:")
        
        if submitted:
            with st.spinner("Processing your game and finding recommendations..."):
                # Prepare user input
                user_input = {
                    'Name': name,
                    'Platform': platform,
                    'Year_of_Release': year,
                    'Genre': genre,
                    'Publisher': publisher,
                    'NA_Sales': na_sales,
                    'EU_Sales': eu_sales,
                    'JP_Sales': jp_sales,
                    'Other_Sales': other_sales,
                    'User_Score': user_score,
                    'Rating': rating
                }
                
                try:
                    # Preprocess the input
                    processed_features = preprocess_user_input(user_input)
                    
                    # Get recommendations
                    recommender = knn_recommender if "KNN" in model_choice_custom else cosine_recommender
                    
                    if model_choice_custom == 'KNN (Euclidean)':
                        # For KNN, we need to use the model directly
                        distances, indices = recommender.model.kneighbors(
                            [processed_features],
                            n_neighbors=num_recs_custom + 1
                        )
                        recommendations = [(recommender.game_names[i], round(d, 4)) 
                                        for i, d in zip(indices[0][1:], distances[0][1:])]
                    else:
                        # For cosine similarity, we need to compute similarity with all games
                        game_features = recommender.data.values
                        similarity_scores = cosine_similarity([processed_features], game_features)[0]
                        top_indices = np.argsort(similarity_scores)[-num_recs_custom-1:-1][::-1]
                        recommendations = [(recommender.game_names[i], round(similarity_scores[i], 4)) 
                                        for i in top_indices]
                    
                    st.toast("Recommendation processed",icon=":material/manufacturing:")
                    st.success("Here are your recommendations:")
                    display_recommendations(recommendations,name)
                    
                except ValueError as e:
                    st.error(str(e))
                    st.error("Please try a different game or check your input.")
    return

if __name__ == "__main__":
    recommend_page()