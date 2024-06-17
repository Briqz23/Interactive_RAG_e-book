import streamlit as st
import requests
import os

def main():
    st.title("Interactive Alice's Wonderland")

    col1, col2 = st.columns(2)

    with col1:
        
        st.write("""
                 
  Alice wandered through the whimsical forest of Wonderland, her eyes wide with curiosity. She stumbled upon a large mushroom, atop which sat a blue Caterpillar, calmly smoking a hookah.

“Who are you?” the Caterpillar asked, his voice slow and deliberate.

“I—I hardly know, sir, just at present,” Alice replied. “At least I know who I was this morning, but I think I must have been changed several times since then.”

The Caterpillar took a long drag from his hookah. “What do you mean by that?” he inquired.

Alice explained, “I've had so many surprising things happen today, I'm not quite sure of myself anymore. How do you manage to stay the same size?”

“One side will make you grow taller, and the other side will make you grow shorter,” said the Caterpillar.

“One side of what? Of the mushroom?” Alice asked eagerly.

“Precisely,” the Caterpillar replied. “Try for yourself. Keep your temper.”

With that, he resumed his smoking, leaving Alice to figure out the mystery of the mushroom on her own. She carefully broke off a piece from each side, wondering what adventures lay ahead with each bite.
        """)
    
    with col2:
        character_options = [
            "Alice",
            "White Rabbit",
            "Mad Hatter",
            "Cheshire Cat",
            "Queen of Hearts"
        ]

        selected_character = st.selectbox("Select a character", character_options)

        character_images = {
            "Alice": "../main_image_project/outputs/Alice/04.png",
            "White Rabbit": "../main_image_project/outputs/Caterpillar/05.png",
            "Mad Hatter": "../main_image_project/outputs/Mad_Hatter/05.png",
            "Cheshire Cat": "../main_image_project/outputs/Cheshire_Cat/05.png",
            "Queen of Hearts": "../main_image_project/outputs/Queen_of_Hearts/01.png"
        }

        image_path = character_images[selected_character]
        if os.path.exists(image_path):
            st.image(image_path, caption=selected_character, use_column_width=True)
        else:
            st.error(f"Image for {selected_character} not found at {image_path}")

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