import streamlit as st
from gpt4 import get_workout_plan
from db import create_workout, get_latest_workout, get_user_by_email

# Page styling
#st.set_page_config(page_title="Workout Planner", page_icon="💪", layout="wide")

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
    .workout-box {
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
        text-align: center;
    }
    .info-text {
        font-size: 16px;
        color: #7D3C98;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Ensure user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("You need to log in to access this page.")
else:
    user_email = st.session_state['email']
    user = get_user_by_email(user_email)

# Workout Planner Title
st.markdown("<h1 class='title'>💪 Workout Planner</h1>", unsafe_allow_html=True)

# Image at the top
st.image("./assets/workout.jpg", use_column_width=True, caption="Your Personalized Workout Plan")

# Fetch and display latest workout plan
latest_workout = get_latest_workout(user['_id'])
if latest_workout:
    st.markdown("<h2 class='subtitle'>Latest Workout Plan</h2>", unsafe_allow_html=True)
    plan = "\n".join(latest_workout['workout_plan'])
    st.markdown(f"<div class='workout-box'>{plan}</div>", unsafe_allow_html=True)
    #for workout in latest_workout['workout_plan']:
        #st.markdown(f"{workout}") #st.markdown(f"<div class='workout-box'>{workout}</div>", unsafe_allow_html=True)

# Button to generate a new workout plan
if st.button("Generate New Workout Plan", key='generate-workout'):
    workout_plan = get_workout_plan(user).split('\n')
    st.markdown("<h2 class='subtitle'>Your New Workout Plan</h2>", unsafe_allow_html=True)
    plan = "\n".join(workout_plan)
    st.markdown(f"<div class='workout-box'>{plan}</div>", unsafe_allow_html=True)
    #for workout in workout_plan:
        #st.markdown(f"<div class='workout-box'>{workout}</div>", unsafe_allow_html=True)

    create_workout(user['_id'], workout_plan)

# Footer or closing note
st.markdown("---")
st.markdown("<p class='info-text'>Consistency is key! Keep up with your workout routine and make small improvements every day.</p>", unsafe_allow_html=True)
