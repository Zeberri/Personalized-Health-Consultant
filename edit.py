import streamlit as st
from db import get_user_by_email, update_user_info
from datetime import datetime


def main():
    # Ensure user is logged in
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("You need to log in to access this page.")
    else:
        user_email = st.session_state['email']
        user = get_user_by_email(user_email)

    with st.form("edit_form"):
        new_name = st.text_input("Name", value=user['name'])
        new_age = st.number_input("Age", value=user['age'], min_value=1, max_value=120)
        new_gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(user['gender']))
        new_weight = st.number_input("Weight (kg)", value=user['weight'])
        new_height = st.number_input("Height (cm)", value=user['height'])
        new_medical_conditions = st.text_input("Medical Conditions", value=user['medical_conditions'])
        new_health_goals = st.text_input("Health Goals", value=user['health_goals'])

        # Add a submit button to save changes
        submitted = st.form_submit_button("Save Changes")
        if submitted:
            # Update the user information in the database
            user = {
                "name": new_name,
                "email": user_email,
                "age": new_age,
                "gender": new_gender,
                "height": new_height,
                "weight": new_weight,
                "medical_conditions": new_medical_conditions,
                "health_goals": new_health_goals,
                "created_at": datetime.now()
            }
            result = update_user_info(user_email, user)
            if result == True:
                st.success("Your information has been updated!")
            else:
                st.error("Something went Wrong...")
                st.error("Failed to Update User Info")

if __name__ == "__main__":
    main()