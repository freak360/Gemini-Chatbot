import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Defining model parameters
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Defining a function to get a response from our model
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


# Defining the main function to initialize the streamlit app
st.set_page_config(page_title="Q&A Bot", page_icon="🤖")
st.header("Gemini Chatbot")

#Initialize the session state for chat history if it does not exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask Question")

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session chat history
    st.session_state['chat_history'].append(("You",input))
    st.subheader("Response:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot",chunk.text))

st.subheader("The chat history is: ")
for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")

