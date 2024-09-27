import streamlit as st
import requests
import json
import base64


# Function to get the response from the API
def get_ai_response(message):
    token = st.secrets['ASTRA_TOKEN']

    # URL and headers
    url = "https://api.langflow.astra.datastax.com/lf/aa351095-cc82-4a0a-9c99-739298e5ab5b/api/v1/run/dce5ff70-673e-4e16-bb78-1da3b0f3356b?stream=false"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # Payload
    data = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {
            "ChatInput-W8IIn": {},
            "AstraVectorStoreComponent-B8Nfo": {},
            "ParseData-oBaYw": {},
            "Prompt-d9dmO": {},
            "ChatOutput-Jq7eq": {},
            "SplitText-nmHYX": {},
            "File-myQB4": {},
            "AstraVectorStoreComponent-flRbw": {},
            "OpenAIEmbeddings-fJoXA": {},
            "OpenAIEmbeddings-fOiFN": {},
            "OpenAIModel-lCtaS": {}
        }
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check the response
    if response.status_code == 200:
        response_data = response.json()
        # Extract the 'text' field from the response
        text_message = response_data['outputs'][0]['outputs'][0]['results']['message']['data']['text']
        return text_message
    else:
        return f"Failed to get response. Status code: {response.status_code}"


# Start with empty messages, stored in session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to add background image
# Function to add background image from a local file
# Function to add background image with transparency
def add_bg_from_local(image_file, opacity=0.5):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})), url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Draw a title and some markdown
st.title("Your personal Efficiency Booster")
st.markdown("""Generative AI is considered to bring the next Industrial Revolution.  
Why? Studies show a **37% efficiency boost** in day to day work activities!""")

# Draw all messages, both user and bot so far (every time the app reruns)
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

# Draw the chat input box
if question := st.chat_input("What's up?"):
    # Store the user's question in a session object for redrawing next time
    st.session_state.messages.append({"role": "human", "content": question})

    # Draw the user's question
    with st.chat_message('human'):
        st.markdown(question)

    # Get the AI response
    answer = get_ai_response(question)

    # Store the bot's answer in a session object for redrawing next time
    st.session_state.messages.append({"role": "ai", "content": answer})

    # Draw the bot's answer
    with st.chat_message('assistant'):
        st.markdown(answer)
