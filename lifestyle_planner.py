import streamlit as st
from gpt4 import get_lifestyle_plan
from db import create_plan, get_latest_plan, get_user_by_email

# Page styling
#st.set_page_config(page_title="Lifestyle Planner", page_icon="🌿", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #2874A6;
        text-align: center;
    }
    .subtitle {
        font-size: 22px;
        font-weight: bold;
        color: #2E86C1;
    }
    .plan-box {
        background-color: #abc0d4;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        color: #1C2833;
        border: 1px solid #AAB7B8;
        margin-bottom: 10px;
    }
    .generate-button {
        background-color: #2ECC71;
        color: white;
        font-size: 18px;
        padding: 10px;
        border-radius: 8px;
        margin-top: 20px;
    }
    .responsive-image {
        width: 100%;
        max-width: 400px;  /* Max width on larger screens */
        height: auto;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Ensure user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("You need to log in to access this page.")
else:
    user_email = st.session_state['email']
    user = get_user_by_email(user_email)

# Lifestyle Planner Title
st.markdown("<h1 class='title'>🌿 Lifestyle Planner</h1>", unsafe_allow_html=True)

# Image at the top
st.image("./assets/lifestyle.png", use_column_width="auto", caption="Your Personalized Lifestyle Plan")

# Fetch and display latest lifestyle plan
latest_plan = get_latest_plan(user['_id'])
if latest_plan:
    st.markdown("<h2 class='subtitle'>Latest Lifestyle Plan</h2>", unsafe_allow_html=True)
    plan = "\n".join(latest_plan['lifestyle_plan'])
    st.markdown(f"<div class='plan-box'>{plan}</div>", unsafe_allow_html=True)
    #for plan in latest_plan['lifestyle_plan']:
    #   st.markdown(f"{plan}") #<div class='plan-box'>{plan}</div>", unsafe_allow_html=True)

# Button to generate a new lifestyle plan
if st.button("Generate New Lifestyle Plan", key='generate-plan'):
    lifestyle_plan = get_lifestyle_plan(user).split('\n')
    st.markdown("<h2 class='subtitle'>Your New Lifestyle Plan</h2>", unsafe_allow_html=True)
    plan = "\n".join(lifestyle_plan)
    st.markdown(f"<div class='plan-box'>{plan}</div>", unsafe_allow_html=True)
    #for plan in lifestyle_plan:
    #    st.markdown(f"{plan}") #<div class='plan-box'>{plan}</div>", unsafe_allow_html=True)
        
    create_plan(user['_id'], lifestyle_plan)

# Footer or closing note
st.markdown("---")
st.markdown("<p class='info-text'>Remember, small lifestyle changes can lead to big improvements over time. Stay consistent!</p>", unsafe_allow_html=True)
