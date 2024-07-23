import streamlit as st
from openai import OpenAI
import time

st.title(':robot_face: CV Nao')

# Initialize chat history (using session_state)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.markdown(f"*Tú:* {message['content']}")
    elif message['role'] == 'assistant':
        st.markdown(f"*CV NAO:* {message['content']}")

# Function to clear the input field
def clear_input():
    st.session_state.user_input = ""

# Text input for user query
user_input = st.text_area("Escribe tu mensaje:", key="user_input", height=200)

# Input for OpenAI API key
user_input_key = st.text_input("API KEY OPEN IA:", type="password")

# Initialize OpenAI client
if user_input_key:
    client = OpenAI(api_key=user_input_key)

def handle_submit():
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.user_input = ""  # Clear the input

        # Create thread and message
        thread = client.beta.threads.create()
        thread_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id='asst_ItqB5rVYTpd9dCuVXoiP05mt'  # Replace with your assistant ID
        )

        # Wait for the run to complete
        with st.spinner("Thinking..."):
            while run.status != "completed":
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                time.sleep(0.5)

        # Retrieve and display the response
        messages = client.beta.threads.messages.list(thread_id=thread.id).data
        latest_message = messages[0]
        response_text = latest_message.content[0].text.value
        
        # Extract the text content correctly
        if isinstance(latest_message.content, list):
            response_text = latest_message.content[0].text.value
        else:
            response_text = latest_message.content

        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_text})

# The button will trigger the callback to handle the submit action
st.button("Enviar", on_click=handle_submit)
