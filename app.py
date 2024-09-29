import streamlit as st
from signup import signup_page, login_page
from db import get_user_by_email
#from first import login

def login():
    st.sidebar.title("Sign Up / Login")
    choice = st.sidebar.radio("Select an option", ["Login", "Sign Up"])
    if choice == "Login":
        login_page()
    else:
        signup_page()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login()
    else:
        #st.sidebar.title("Health Assistant")

        # Place the logout button in the sidebar
        #if st.sidebar.button("Log Out"):
        #    st.session_state['logged_in'] = False
        #    st.session_state.pop('email', None)
        #    st.switch_page("first.py")
        #    st.experimental_rerun()  # This will reset the page and show the login page

        user_email = st.session_state['email']
        user = get_user_by_email(user_email)


        page = st.navigation([
            st.Page("dashboard.py", url_path='dashboard', title="Dashboard", icon="🩺"),
            st.Page("lifestyle_planner.py", url_path='lifestyle', title="Lifestyle", icon="🌿"),
            st.Page("workout_planner.py", url_path='workout', title="Workout", icon="💪"),
            st.Page("chatbot.py", url_path='consultation', title="Consultation", icon="👩🏾‍⚕️"),
            st.Page("doctor_calendar.py", url_path='doctor_calender', title="Doctor's Visit", icon="🏫")
        ])
        page.run()


if __name__ == "__main__":
    main()
