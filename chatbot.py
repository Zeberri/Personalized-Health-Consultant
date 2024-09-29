import streamlit as st
from gpt4 import chat_gpt4
import time
from db import create_consultation_log, get_user_by_email

# Make sure the user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("You need to log in to access this page.")
else:
    user_email = st.session_state['email']
    user = get_user_by_email(user_email)

#def chatbot_page(user):

st.title("Health Consultation")

# Display avatar image
avatar_url = "./assets/doctor.jpg"  # Replace with the URL of your avatar image
st.image(avatar_url) #width=300)

# Animated introductory text
intro_text = f"""
<style>
.intro-text {{
    font-size: 20px;
    font-style: italic;
    animation: slideIn 2s ease-out;
}}
@keyframes slideIn {{
    from {{
        opacity: 0;
        transform: translateX(-100%);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}
</style>
<div class="intro-text">
    Hello {user['name']}, I am Tarela your Personal Health Consultant. How can I assist you today?
</div>
"""
st.markdown(intro_text, unsafe_allow_html=True)

# Delay for animation effect before showing the chat input
time.sleep(2)

# Ensure that user is stored in session state
if "user" not in st.session_state:
    st.session_state.user = user  # Initialize user in session state

# Create an input to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_input = st.chat_input("Ask your health question here...")

if user_input:
    # Add user's message to chat history and display it
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Send user's message to GPT-4 for response
    response = chat_gpt4(user_input, user)  # Process the message using gpt4.py

    # Log the consultation in the database
    create_consultation_log(st.session_state.user['_id'], user_input, response)

    # Add the assistant's response to the chat history and display it
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
