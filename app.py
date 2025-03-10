import streamlit as st
import json

# Function to load data from a JSONL file
@st.cache_data
def load_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

# Load the JSONL data
data = load_data('scrape_results.jsonl')  # Change file path as needed

# Initialize session state to track the current index
if 'index' not in st.session_state:
    st.session_state.index = 0

# Display the current dictionary in a pretty JSON format
st.json(data[st.session_state.index])

# Create columns for navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Previous"):
        if st.session_state.index > 0:
            st.session_state.index -= 1
with col2:
    if st.button("Next"):
        if st.session_state.index < len(data) - 1:
            st.session_state.index += 1

# Display record number info
st.write(f"Record {st.session_state.index + 1} of {len(data)}")
