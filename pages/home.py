import streamlit as st

def home_page():
    st.markdown("""<style>
        .center-title {
            text-align: center;
            margin-top: 0;
            margin-bottom: 2rem;
        }
        .footer {
            background-color: #000;
            color: #fff;
            text-align: center;
            padding: 1rem 0;
            margin-top: 3rem;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<h1 class="center-title" style="font-size: 6rem;">TECHWILL x GAME</h1>', unsafe_allow_html=True)

    col1,col2=st.columns(2)
    st.markdown("""<style>.stVerticalBlock.st-key-con11hp {background-color: #4b9cd3; color: white; padding: 20px; border-radius: 10px; transition: all 0.3s ease-in-out;} .stVerticalBlock.st-key-con11hp:hover {background-color: rgba(242,240,239,0.5); color: black; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); transform: translateY(-2px);} </style>""", unsafe_allow_html=True)
    con=col1.container(border=True,key="con11hp")
    with con:
        st.markdown("""
        ## 🎮 Game Recommender System
        - **Smart Matching** • Uses both KNN & cosine similarity for accuracy  
        - **Feature-Rich** • Analyzes 320+ attributes including sales, ratings, and genres  
        - **Two Modes** • Works with existing games or custom user-created profiles  
        - **Instant Results** • Delivers personalized picks in seconds with clear scoring  
        - **Visual Proof** • Interactive charts justify every recommendation  
        - **Cloud-Powered** • Google Cloud integration ensures scalable performance  
        """)

    con=col2.container(border=True,key="con12hp")
    st.markdown("""<style>.stVerticalBlock.st-key-con12hp {background-color: #4b9cd3; color: white; padding: 20px; border-radius: 10px; transition: all 0.3s ease-in-out;} .stVerticalBlock.st-key-con12hp:hover {background-color: rgba(242,240,239,0.5); color: black; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); transform: translateY(-2px);} </style>""", unsafe_allow_html=True)
    with con:
        st.markdown("""
        ## 🤖 Model Building
        - **KNN Algorithm** • Uses Euclidean distance to find closest game matches  
        - **Cosine Similarity** • Measures vector angles for thematic recommendations  
        - **Dual Approach** • Combines both methods for comprehensive results  
        - **Feature-Rich** • Analyzes 320+ game attributes for precision  
        - **Optimized** • Pre-trained models for instant predictions  
        - **Transparent Results** • Clear metrics show recommendation quality  
        """)
    
    st.markdown("""<style>.stVerticalBlock.st-key-con2hp {background-color: #4b9cd3; color: white; padding: 20px; border-radius: 10px; transition: all 0.3s ease-in-out;} .stVerticalBlock.st-key-con2hp:hover {background-color: rgba(242,240,239,0.5); color: black; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); transform: translateY(-2px);} </style>""", unsafe_allow_html=True)
    con=st.container(border=True,key="con2hp")
    with con:
        st.markdown("""
        ## ✨ Key Advantages
        - **Personalized Experience** • Tailors recommendations to individual preferences  
        - **Discovery Engine** • Uncovers hidden gems in your game library  
        - **Time Saver** • Quickly finds matches instead of manual searching  
        - **Data-Driven** • Uses objective metrics beyond just genres  
        - **Adaptable** • Works for both existing and custom game profiles  
        - **Visual Insights** • Clear charts show why games were recommended  
        """)

    col1,col2=st.columns(2)
    st.markdown("""<style>.stVerticalBlock.st-key-con31hp {background-color: #4b9cd3; color: white; padding: 20px; border-radius: 10px; transition: all 0.3s ease-in-out;} .stVerticalBlock.st-key-con31hp:hover {background-color: rgba(242,240,239,0.5); color: black; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); transform: translateY(-2px);} </style>""", unsafe_allow_html=True)
    con=col1.container(border=True,key="con31hp")
    with con:
        st.markdown("""
        ## 🚀 Feature Engineering
        - **One-Hot Encoding**: Applied to categorical columns (`Platform`, `Genre`, etc.)
        - **Numerical Scaling**: MinMaxScaler for sales metrics and user scores
        - **Final Features**: 320 dimensions (numeric + one-hot encoded)""")

    st.markdown("""<style>.stVerticalBlock.st-key-con32hp {background-color: #4b9cd3; color: white; padding: 20px; border-radius: 10px; transition: all 0.3s ease-in-out;} .stVerticalBlock.st-key-con32hp:hover {background-color: rgba(242,240,239,0.5); color: black; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); transform: translateY(-2px);} </style>""", unsafe_allow_html=True)
    con=col2.container(border=True,key="con32hp")
    with con:
        st.markdown("""
        ## 🛠️ Technologies Used  
        - Python • Streamlit • Scikit-learn  
        - Google Cloud • Railway • MySQL  
        - Plotly • Pandas • Joblib """)

    # Footer
    st.markdown("""
    <div class="footer">
        © Aakash Kharb
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    home_page()
