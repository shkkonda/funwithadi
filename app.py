import streamlit as st
import json

# Define the function to extract the cleaned markdown text
def extract_text(text):
    # Define the exact prefix to search for
    prefix = "(Reuters) -"
    start_index = text.find(prefix)
    if start_index == -1:
        return None

    # Extract the text after the prefix and strip extra whitespace
    extracted = text[start_index + len(prefix):].strip()
    
    # Define the exact chunk to remove (including newlines and spacing)
    removal_chunk = """Share

- X

- Facebook

- Linkedin

- Email

- Link"""
    
    # Look for the removal chunk in the extracted text
    chunk_index = extracted.find(removal_chunk)
    if chunk_index != -1:
        # Remove the entire chunk and everything after it
        extracted = extracted[:chunk_index].strip()
    
    return extracted

# Function to load data from a JSONL file and clean the markdown text if available
@st.cache_data
def load_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            record = json.loads(line)
            # If the record has a nested 'response' -> 'markdown' field, clean it.
            if 'response' in record and 'markdown' in record['response']:
                cleaned = extract_text(record['response']['markdown'])
                # Replace the original markdown with the cleaned version if extraction was successful
                if cleaned is not None:
                    record['response']['markdown'] = cleaned
            data.append(record)
    return data

# Load the JSONL data (adjust the file path as needed)
data = load_data('scrape_results.jsonl')

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
