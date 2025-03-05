import os 
import streamlit as st
from pymongo import MongoClient
from datetime import datetime
uri = st.secrets["MONGODB_CONNECTIONSTRING"]
database = st.secrets["MONGODB_DATABASE"]

client = MongoClient(uri)
db = client[database]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Could not ping Database: {e}")


# User-related operations
def create_user(name, email, password, age, gender, height, weight, medical_conditions, health_goals):
    user = {
        "name": name,
        "email": email,
        "password": password,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "medical_conditions": medical_conditions,
        "health_goals": health_goals,
        "created_at": datetime.now()
    }
    db.users.insert_one(user)

def get_user_by_email(email):
    return db.users.find_one({"email": email})

def update_user_info(user_email, updated_info):
    """
    Update the user information in the database.

    :param user_email: Email of the user whose information needs to be updated.
    :param updated_info: Dictionary containing the updated user information.
    :return: True if the update is successful, otherwise False.
    """
    try:
        # Find the user by email and update their info
        result = db.users.update_one(
            {"email": user_email},  # Find user by email
            {"$set": updated_info}  # Update user info
        )

        # Check if the update was successful
        if result.modified_count > 0:
            print("User information updated successfully!")
            return True
        else:
            print("No changes were made.")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Plan-related operations
def create_plan(user_id, lifestyle_plan):
    plan = {
        "user_id": user_id,
        "lifestyle_plan": lifestyle_plan,
        "created_at": datetime.now()
    }
    db.user_plans.insert_one(plan)

def get_latest_plan(user_id):
    return db.user_plans.find_one({"user_id": user_id}, sort=[("created_at", -1)])

# Workout-related operations
def create_workout(user_id, workout_plan):
    workout = {
        "user_id": user_id,
        "workout_plan": workout_plan,
        "created_at": datetime.now()
    }
    db.workouts.insert_one(workout)

def get_latest_workout(user_id):
    return db.workouts.find_one({"user_id": user_id}, sort=[("created_at", -1)])

# Consultation logs
def create_consultation_log(user_id, question, response):
    log = {
        "user_id": user_id,
        "question": question,
        "response": response,
        "created_at": datetime.now()
    }
    db.consultations.insert_one(log)

def get_consultation_log(user_id):
    return db.consultations.find({"user_id": user_id})

# Doctor visit scheduling
def schedule_doctor_visit(user_id, visit_reason, appointment_date):
    visit = {
        "user_id": user_id,
        "visit_reason": visit_reason,
        "appointment_date": appointment_date,
        "created_at": datetime.now()
    }
    db.doctor_visits.insert_one(visit)

def get_doctor_visits(user_id):
    return db.doctor_visits.find({"user_id": user_id}).sort("appointment_date", 1)

# Workout-related operations
def create_health_recommendation(user_id, recommend):
    recommendation = {
        "user_id": user_id,
        "Health_Recommendation": recommend,
        "created_at": datetime.now()
    }
    db.recommendations.insert_one(recommendation)

def get_health_recommendation_db(user_id):
    return db.recommendations.find_one({"user_id": user_id}, sort=[("created_at", -1)])