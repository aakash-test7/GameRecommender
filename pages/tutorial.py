import streamlit as st
from backend import init_gcs_client

def tutorial_page():
    st.title("Tutorials Page")
    st.write("**Learn how to use this interface**")
    
    from datetime import  timedelta
    import os
    client = init_gcs_client()
    def generate_signed_url(blob_name, expiration_minutes=30):
        """Generate a signed URL for temporary access to a GCS object"""
        if not client:
            st.error("GCS client not initialized")
            return None
            
        try:
            bucket = client.bucket("recommender-2025")
            blob = bucket.blob(blob_name)
            
            if not blob.exists():
                st.error(f"File {blob_name} not found in GCS")
                return None
                
            url = blob.generate_signed_url(
                version="v4",
                expiration=timedelta(minutes=expiration_minutes),
                method="GET"
            )
            return url
        except Exception as e:
            st.error(f"Error generating signed URL: {str(e)}")
            return None

    video_url = generate_signed_url("Videos/video1.mp4")
    if video_url:
        st.video(video_url, start_time=0)
    else:
        st.warning("Could not generate streaming URL")


if __name__ == "__main__":
    tutorial_page()

