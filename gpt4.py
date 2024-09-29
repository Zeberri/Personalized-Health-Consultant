import os
import requests
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from db import get_consultation_log
load_dotenv()

# Configuration for Azure OpenAI
API_KEY = os.getenv("AZURE_API_KEY")  # Set this in your environment
ENDPOINT = "https://fupre-chatbot-dev.openai.azure.com/openai/deployments/gpt-35-turbo-16k-2-Tarela/chat/completions?api-version=2024-05-01-preview"

# Azure headers
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

# Helper function to query GPT-4
def query_gpt4(prompt):
    SYSTEM_MESSAGE = """
        You are an AI assistant dedicated to helping users with personalized health recommendations. Based on the information provided, you offer thoughtful, detailed, and actionable advice tailored to their specific needs, such as lifestyle plans, workout routines, or general health guidance.
        Ensure that your recommendations are clear, concise, and easy to follow. Provide practical steps the user can take, without overloading them with unnecessary details. Keep your explanations informative, but to the point, focusing on delivering value in each suggestion.
        Always maintain a supportive and encouraging tone, ensuring the user feels empowered to follow your advice.
    """
    # Define payload as per Azure OpenAI template
    payload = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": SYSTEM_MESSAGE
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 1500
    }

    try:
        # Send the request to Azure OpenAI API
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Raises an exception if there's an error

        # Parse the response JSON
        result = response.json()

        # Extract the assistant's reply from the response
        assistant_reply = result['choices'][0]['message']['content']
        print(f"assistant reply: {assistant_reply}")
        return assistant_reply
    
    except requests.RequestException as e:
        print(f"Failed to query GPT-4. Error: {e}")
        return None

#Function to chat
def chat_gpt4(prompt, user):
    chat_history_cursor = get_consultation_log(user['_id'])
    # Initialize an empty list for chat history
    chat_history = []

    # Iterate over the cursor to extract individual documents
    for history in chat_history_cursor:
        chat_history.append({
            'question': history['question'],
            'response': history['response'],
            'created_at': history['created_at']
        })

    print(f"Chat History: {chat_history[-5:]}")

    SYSTEM_MESSAGE = f"""
        You are Tarela, a friendly and caring health consultant chatbot. Your goal is to make the user feel comfortable and confident in sharing their health concerns while offering thoughtful, straightforward advice.

        Here is some background on the user:
        - Name: {user['name']}
        - Age: {user['age']}
        - Gender: {user['gender']}
        - Weight: {user['weight']} kg
        - Height: {user['height']} cm
        - Medical Conditions: {user['medical_conditions']}
        - Health Goals: {user['health_goals']}

        Here is the user's chat history with you: {chat_history[-5:]}.

        Always engage the user with warmth and empathy. Keep your responses very short, supportive, easy to understand, and in a conversational manner. Ask questions one at a time, and avoid overwhelming the user with too much information at once. Focus on providing practical advice that the user can easily follow, while showing understanding and encouragement. Your tone should be friendly, compassionate, and reassuring.
        Don't greet the User again unless the User greets you.
    """

    # Define payload as per Azure OpenAI template
    payload = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": SYSTEM_MESSAGE
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 1500
    }

    try:
        # Send the request to Azure OpenAI API
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Raises an exception if there's an error

        # Parse the response JSON
        result = response.json()

        # Extract the assistant's reply from the response
        assistant_reply = result['choices'][0]['message']['content']
        print(f"assistant reply: {assistant_reply}")
        return assistant_reply
    
    except requests.RequestException as e:
        print(f"Failed to query GPT-4. Error: {e}")
        return None
    

# Health recommendations based on user data
def get_health_recommendations(user):
    prompt = f"""
    Based on the following user data, provide health recommendations:
    - Name: {user['name']}
    - Age: {user['age']}
    - Gender: {user['gender']}
    - Height: {user['height']} cm
    - Weight: {user['weight']} kg
    - Medical Conditions: {user['medical_conditions']}
    - Health Goals: {user['health_goals']}
    """
    return query_gpt4(prompt)

# Generate a lifestyle plan
def get_lifestyle_plan(user):
    prompt = f"""
    Create a personalized daily lifestyle plan for {user['name']}, considering:
    - Age: {user['age']}
    - Gender: {user['gender']}
    - Weight: {user['weight']} kg
    - Height: {user['height']} cm
    - Medical Conditions: {user['medical_conditions']}
    - Health Goals: {user['health_goals']}
    Provide meal plan, hydration goals, and daily lifestyle suggestions.
    """
    return query_gpt4(prompt)

# Generate a workout plan
def get_workout_plan(user):
    prompt = f"""
    Generate a workout routine for {user['name']}:
    - Age: {user['age']}
    - Gender: {user['gender']}
    - Weight: {user['weight']} kg
    - Height: {user['height']} cm
    - Medical Conditions: {user['medical_conditions']}
    - Fitness Goals: {user['health_goals']}
    Provide strength and cardio exercises, with duration and frequency.
    """
    return query_gpt4(prompt)

# Generate health consultation response
def get_gpt4_response(user_input, user):
    prompt = f"""
    {user['name']} is asking the following health question:
    "{user_input}"
    """
    return chat_gpt4(prompt, user)
