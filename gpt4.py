import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from db import get_consultation_log

load_dotenv()

# GitHub OpenAI Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_ENDPOINT = os.getenv("GITHUB_ENDPOINT")
MODEL_NAME = "gpt-4o-mini"

# Initialize OpenAI client
client = OpenAI(base_url=GITHUB_ENDPOINT, api_key=GITHUB_TOKEN)

def query_gpt4(prompt):
    SYSTEM_MESSAGE = """
        You are an AI assistant dedicated to helping users with personalized health recommendations.
        Ensure that your recommendations are clear, concise, and easy to follow.
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            top_p=0.95,
            max_tokens=1500,
            model=MODEL_NAME
        )
        print(response.choices)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Failed to query GPT-4. Error: {e}")
        return None

def chat_gpt4(prompt, user):
    chat_history_cursor = get_consultation_log(user['_id'])
    chat_history = [
        {'question': h['question'], 'response': h['response'], 'created_at': h['created_at']}
        for h in chat_history_cursor
    ]

    SYSTEM_MESSAGE = f"""
        You are Tarela, a friendly and caring health consultant chatbot.
        - Name: {user['name']}
        - Age: {user['age']}
        - Gender: {user['gender']}
        - Weight: {user['weight']} kg
        - Height: {user['height']} cm
        - Medical Conditions: {user['medical_conditions']}
        - Health Goals: {user['health_goals']}
        Here is the user's chat history: {chat_history[-5:]}.
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            top_p=0.95,
            max_tokens=1500,
            model=MODEL_NAME
        )
        print(response.choices)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Failed to query GPT-4. Error: {e}")
        return None

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

def get_gpt4_response(user_input, user):
    prompt = f"""
    {user['name']} is asking the following health question:
    "{user_input}"
    """
    response = chat_gpt4(prompt,user)
    return response