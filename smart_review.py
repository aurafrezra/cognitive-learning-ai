import json
import os
import datetime
import math

USER_DATA_PATH = 'user_data'

def load_user_responses(username):
    file_path = os.path.join(USER_DATA_PATH, f"{username}_responses.json")
    if not os.path.exists(file_path):
        print("❌ No data found for this user.")
        return []

    with open(file_path, 'r') as f:
        return json.load(f)

def calculate_strength(response):
    base = response['correct'] * response['confidence']
    time_then = datetime.datetime.strptime(response['timestamp'], "%Y-%m-%d %H:%M:%S")
    time_now = datetime.datetime.now()
    days_passed = (time_now - time_then).days + 1
    decay = math.exp(-0.1 * days_passed)
    return round(base * decay, 2)

def build_strength_map(responses):
    concept_strength = {}
    for r in responses:
        concept = r['concept']
        score = calculate_strength(r)
        if concept not in concept_strength:
            concept_strength[concept] = []
        concept_strength[concept].append(score)

    avg_strengths = {
        concept: round(sum(scores) / len(scores), 2)
        for concept, scores in concept_strength.items()
    }

    return avg_strengths

def suggest_weak_concepts(strength_map, threshold=3.0):
    weak_concepts = {
        concept: strength
        for concept, strength in strength_map.items()
        if strength < threshold
    }

    # Sort from weakest to strongest
    return dict(sorted(weak_concepts.items(), key=lambda item: item[1]))

def display_review_suggestions(username):
    responses = load_user_responses(username)
    if not responses:
        return

    strength_map = build_strength_map(responses)
    weak_concepts = suggest_weak_concepts(strength_map)

    print(f"\n🔁 Smart Review Suggestions for {username} 🔁\n")

    if not weak_concepts:
        print("🎉 No weak areas found! You're doing great!")
    else:
        for concept, strength in weak_concepts.items():
            status = "🔴 Very Weak" if strength < 2 else "🟡 Needs Review"
            print(f"{concept:25} → Strength: {strength:4} {status}")

if __name__ == "__main__":
    username = input("Enter your name: ").strip()
    display_review_suggestions(username)
