import streamlit as st
import json
import os

# Load responses
def load_responses():
    try:
        with open("data/responses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Display the quiz results nicely
def show_results(responses):
    if not responses:
        st.info("No responses recorded yet.")
        return

    st.subheader("🧠 Quiz Responses & Confidence")
    for entry in responses:
        st.markdown(f"""
        **Concept:** {entry['concept']}  
        ✅ Correct: {"Yes" if entry['correct'] else "No"}  
        📊 Confidence: {entry['confidence']}  
        ⏱️ Time Taken: {entry['time_taken']} seconds  
        📝 Your Answer: {entry['answer']}
        ---
        """)

# Streamlit UI
st.title("🧠 Personalized Cognitive Learning AI")
st.markdown("This app visualizes your concept mastery and tracks what you might forget.")

if st.button("🔄 Load My Learning Data"):
    responses = load_responses()
    show_results(responses)
