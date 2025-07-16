
import streamlit as st
import json
import networkx as nx
import matplotlib.pyplot as plt
import os

# Set Streamlit page config
st.set_page_config(page_title="Personalized Cognitive Learning AI", layout="centered")

st.title("🧠 Personalized Cognitive Learning AI")
st.write("This app visualizes your concept mastery and tracks what you might forget.")

# Load responses
response_file_path = os.path.join("user_data", "riz_responses.json")

try:
    with open(response_file_path, "r") as f:
        responses = json.load(f)
except FileNotFoundError:
    responses = []

# Show load button
if st.button("📥 Load My Learning Data"):
    if not responses:
        st.warning("No responses recorded yet.")
    else:
        st.success("Responses loaded!")

        # Create knowledge graph
        G = nx.DiGraph()
        for r in responses:
            concept = r["concept"]
            correctness = "✅" if r["correct"] else "❌"
            label = f"{concept}\n{correctness} | Conf: {r['confidence']} | Time: {round(r['time_taken'], 1)}s"
            G.add_node(label)

        # Simple edges for visualization
        for i in range(len(G.nodes) - 1):
            source = list(G.nodes)[i]
            target = list(G.nodes)[i + 1]
            G.add_edge(source, target)

        # Plot
        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(12, 6))
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="skyblue",
            node_size=2500,
            font_size=8,
            font_weight="bold",
            edge_color="gray",
        )
        st.pyplot(plt)

# Show raw responses
st.subheader("📊 Your Learning Data")
if responses:
    st.json(responses)
else:
    st.info("No data to show yet.")
