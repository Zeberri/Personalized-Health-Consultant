import streamlit as st
from gpt4 import get_health_recommendations
from db import create_health_recommendation, get_health_recommendation_db, get_user_by_email

# Page styling
#st.set_page_config(page_title="Health Dashboard", page_icon="🩺", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #34495E;
        text-align: center;
    }
    .subtitle {
        font-size: 22px;
        font-weight: bold;
        color: #2E86C1;
    }
    .info-text {
        font-size: 18px;
        color: #566573;
    }
    .highlight {
        font-size: 18px;
        font-weight: bold;
        color: #CB4335;
    }
    .bmi-box {
        background-color: #87CEEB;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        color: #2C3E50;
        border: 1px solid #BDC3C7;
    }
    .recommendations {
        background-color: #abc0d4;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        color: #1C2833;
        border: 1px solid #AAB7B8;
    }
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# Ensure user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("You need to log in to access this page.")
else:
    user_email = st.session_state['email']
    user = get_user_by_email(user_email)

# Dashboard Title
st.markdown("<h1 class='title'>🏥 Health Dashboard</h1>", unsafe_allow_html=True)

# Image at the top
st.image("./assets/dashboard.png", use_column_width=True, caption="Your Personalized Health Dashboard")

# User Information Display
st.markdown(f"<h2 class='subtitle'>Welcome, {user['name']}!</h2>", unsafe_allow_html=True)
st.markdown(f"<p class='info-text'>Age: {user['age']} years</p>", unsafe_allow_html=True)
st.markdown(f"<p class='info-text'>Height: {user['height']} cm</p>", unsafe_allow_html=True)
st.markdown(f"<p class='info-text'>Weight: {user['weight']} kg</p>", unsafe_allow_html=True)

# Calculate and display BMI 
if user['weight'] and user['height'] > 0:
    bmi = user['weight'] / ((user['height'] / 100) ** 2)
    st.markdown(f"<div class='bmi-box'>Your **BMI** is: {bmi:.2f}</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='bmi-box'>Add your Weight and Height to get your **BMI**", unsafe_allow_html=True)

#st.page_link("pages/edit.py", label="Update your Info") #, icon="🏠")
#st.link_button("Go to gallery", "/edit.py")

st.markdown("")

# Health Recommendations Button
if st.button("Get Health Recommendations", key="health-recommendation"):
    recommendations = get_health_recommendations(user)
    st.markdown("<h3 class='subtitle'>Health Recommendations</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='recommendations'>{recommendations}</div>", unsafe_allow_html=True)
    create_health_recommendation(user['_id'], recommendations)

# Previous health recommendations
health_recommendation = get_health_recommendation_db(user['_id'])
if health_recommendation:
    st.markdown("<h3 class='subtitle'>Previous Health Recommendations</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='recommendations'>{health_recommendation['Health_Recommendation']}</div>", unsafe_allow_html=True)

# Footer or Closing statement
st.markdown("---")
st.markdown("<p class='info-text'>Maintaining your health is key to a fulfilling life. Follow your recommendations and stay healthy!</p>", unsafe_allow_html=True)
