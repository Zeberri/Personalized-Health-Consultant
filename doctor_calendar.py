import streamlit as st
from datetime import datetime
from db import schedule_doctor_visit, get_doctor_visits, get_user_by_email

# Page styling
#st.set_page_config(page_title="Doctor Calendar", page_icon="🩺", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #2874A6;
        text-align: center;
    }
    .form-input {
        background-color: #EAECEE;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        color: #2C3E50;
        border: 1px solid #BDC3C7;
        margin-bottom: 10px;
    }
    .visit-box {
        background-color: #abc0d4;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        color: #1C2833;
        border: 1px solid #AAB7B8;
        margin-bottom: 10px;
    }
    .schedule-button {
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

# Doctor Calendar Title
st.markdown("<h1 class='title'>🩺 Schedule a Doctor Visit</h1>", unsafe_allow_html=True)

# Input fields for scheduling a visit
with st.form(key="visit_form"):
    visit_reason = st.text_input("Reason for the visit:")
    appointment_date = st.date_input("Select a date")
    appointment_time = st.time_input("Select a time")
    
    if st.form_submit_button("Schedule Visit"):  # Removed the key argument here
        if visit_reason and appointment_date and appointment_time:
            # Combine date and time
            appointment_datetime = datetime.combine(appointment_date, appointment_time)
            schedule_doctor_visit(user['_id'], visit_reason, appointment_datetime)
            st.success("Visit scheduled successfully!")
        else:
            st.error("Please fill in all fields.")

# Display the scheduled visits in a cleaner format
st.markdown("<h2 class='title'>Scheduled Visits Calendar</h2>", unsafe_allow_html=True)

visits = get_doctor_visits(user['_id'])

if visits:

    # Get the current date and time
    current_datetime = datetime.now()

    # Filter out past visits
    upcoming_visits = [visit for visit in visits if visit['appointment_date'] > current_datetime]

    for visit in upcoming_visits:
        st.markdown(f"""
            <div class='visit-box'>
                <strong>Reason:</strong> {visit['visit_reason']}<br>
                <strong>Date:</strong> {visit['appointment_date'].strftime('%Y-%m-%d %H:%M')}
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("<p class='info-text'>No scheduled visits.</p>", unsafe_allow_html=True)
