import streamlit as st
import requests
from urllib.parse import quote
def main():
    st.title("Alice's Wonderland Character Interaction")

    character_options = [
        "Alice",
        "White Rabbit",
        "Mad Hatter",
        "Cheshire Cat",
        "Queen of Hearts"
    ]

    selected_character = st.selectbox("Select a character", character_options)

    prompt = st.text_area("Enter your prompt")

    if st.button("Submit"):
        response = interact_with_character(selected_character, prompt)
        display_response(response)

def interact_with_character(character, prompt):
    url = f"http://localhost:8000/{character.lower().replace(' ', '-')}"
    try:
        response = requests.post(url, json={"prompt": prompt})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error interacting with character: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    return {}

def display_response(response):
    if isinstance(response, dict):
        if "output" in response:
            st.write(response["output"])
        else:
            st.error("Unexpected response format")
    else:
        st.write(response)

if __name__ == "__main__":
    main()