import json
import time
import os
import datetime



# Load knowledge graph from JSON
with open("../graph/graph_data.json", "r") as f:
    graph = json.load(f)

# Flatten concepts into a question list
concepts = list(graph.keys())
for children in graph.values():
    concepts.extend(children)
concepts = list(set(concepts))  # remove duplicates

# Shuffle if you want
import random
random.shuffle(concepts)

# Create user_data directory if it doesn't exist
os.makedirs("../user_data", exist_ok=True)

# Start quiz
username = input("Enter your name: ")
filename = f"../user_data/{username}_responses.json"
responses = []

print("\n📘 Starting Quiz - Newton's Laws Concepts")
print("Type 'exit' anytime to stop.\n")

for concept in concepts:
    print(f"🔹 Concept: {concept}")
    input("Press Enter when ready to answer...")

    start_time = time.time()
    user_answer = input(f"✍️ What do you know about '{concept}'? Write a short explanation:\n")
    time_taken = round(time.time() - start_time, 2)

    if user_answer.lower() == "exit":
        break

    correct = input("✅ Did you get it correct? (y/n): ").strip().lower() == "y"
    confidence = int(input("📊 Confidence level (1-5): "))

    responses.append({
        "concept": concept,
        "answer": user_answer,
        "correct": correct,
        "confidence": confidence,
        "time_taken": time_taken
    })

    print("✅ Recorded.\n")

# Save responses
with open(filename, "w") as f:
    json.dump(responses, f, indent=2)

print(f"\n🎉 Quiz complete! Responses saved to: {filename}")
