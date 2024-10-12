# career_recommender_app.py

import streamlit as st
import pandas as pd
from collections import defaultdict

# Load career data
@st.cache
def load_career_data():
    return pd.read_csv('career_data.csv')

career_data = load_career_data()

# Function to calculate scores
def calculate_scores(user_profile, careers):
    scores = defaultdict(int)
    weights = {
        'Skills': 3,
        'Interests': 2,
        'Education': 2,
        'Personality': 1
    }
    
    for index, row in careers.iterrows():
        for category in user_profile:
            user_items = set([item.strip().lower() for item in user_profile[category]])
            career_items = set([item.strip().lower() for item in row[category].split(',')])
            matches = user_items.intersection(career_items)
            scores[row['Career']] += weights[category] * len(matches)
    
    return scores

# Streamlit App
def main():
    st.title(" Career Recommendation System ")
    st.write("Find the best career paths that match your skills, interests, education, and personality traits.")

    st.sidebar.header("Enter Your Profile")
    
    # Collect user inputs
    user_skills = st.sidebar.text_input("Skills (separated by commas)")
    user_interests = st.sidebar.text_input("Interests (separated by commas)")
    user_education = st.sidebar.text_input("Education (separated by commas)")
    user_personality = st.sidebar.text_input("Personality Traits (separated by commas)")
    
    if st.sidebar.button("Get Recommendations"):
        # Process user inputs
        user_profile = {
            'Skills': user_skills.split(','),
            'Interests': user_interests.split(','),
            'Education': user_education.split(','),
            'Personality': user_personality.split(',')
        }
        
        # Calculate scores
        scores = calculate_scores(user_profile, career_data)
        
        # Sort careers based on scores
        sorted_careers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Convert to DataFrame for better display
        recommendations = pd.DataFrame(sorted_careers, columns=['Career', 'Score'])
        
        # Display top 5 recommendations
        st.subheader("Top Career Recommendations")
        st.table(recommendations.head(5))
        
        # Optionally, display all recommendations
        with st.expander("Show All Recommendations"):
            st.table(recommendations)
        
if __name__ == "__main__":
    main()
