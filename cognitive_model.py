import json
import os
import datetime
import math

USER_DATA_PATH = 'user_data'

def load_user_responses(username):
    file_path = os.path.join(USER_DATA_PATH, f"{username}_responses.json")
    if not os.path.exists(file_path):
        print("No data found for this user.")
        return []

    with open(file_path, 'r') as f:
        return json.load(f)

def calculate_strength(response):
    # Base score: correct answer × confidence
    base = response['correct'] * response['confidence']
    
    # Time since answered (in days)
    time_then = datetime.datetime.strptime(response['timestamp'], "%Y-%m-%d %H:%M:%S")
    time_now = datetime.datetime.now()
    days_passed = (time_now - time_then).days + 1  # avoid div by 0

    # Decay function: exponential decay
    decay = math.exp(-0.1 * days_passed)

    return round(base * decay, 2)

def analyze_user(username):
    responses = load_user_responses(username)
    if not responses:
        return

    concept_strength = {}

    for r in responses:
        concept = r['concept']
        score = calculate_strength(r)

        if concept not in concept_strength:
            concept_strength[concept] = []

        concept_strength[concept].append(score)

    print(f"\n📊 Cognitive Strength Report for {username}\n")
    for concept, scores in concept_strength.items():
        avg_strength = round(sum(scores) / len(scores), 2)
        status = "🟢 Strong" if avg_strength > 3.5 else "🟡 Weak" if avg_strength > 2 else "🔴 Fading"
        print(f"{concept:20} → Strength: {avg_strength:4} {status}")

if __name__ == "__main__":
    user = input("Enter your name: ").strip()
    analyze_user(user)
