import os
import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from dotenv import load_dotenv
import re
import pyttsx3
from transformers import pipeline

# Load environment variables
load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model
generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 400,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
]

model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings)

chat = model.start_chat(history=[])
condition = 'You are a compassionate and professional therapist with extensive experience in helping people navigate their mental health challenges. Engage in a text-based therapy session, actively listening to the user\'s concerns and validating their feelings. Ask open-ended questions to encourage the user to share more about their thoughts and experiences, providing evidence-based coping strategies and suggestions tailored to their situation. Maintain a calm, warm, empathetic, and supportive demeanor throughout the conversation, focusing on the user\'s strengths and progress. If the user\'s condition appears to be worsening or they express thoughts of self-harm or severe distress, gently suggest they seek immediate help and provide the helpline number at the end of the conversation: Try contacting AASRA. 91-9820466726. Answer in a minimum of 2 and maximum of 3-4 sentences. Here is the conversation:'

# Function to get response from Gemini model
def get_gemini_response(question, chat_history, emotions):
    conversation = '\n'.join([f"{role}: {text}" for role, text in chat_history])
    emotion_text = "Detected emotions: " + ', '.join([f"{emotion['label']} ({emotion['score']:.2f})" for emotion in emotions])
    full_message = f"{condition}\n{conversation}\nUser: {question}\n{emotion_text}"
    response = chat.send_message(full_message, stream=True)
    response.resolve()  # Wait for the response to complete
    
    if response and hasattr(response, 'text'):
        return response.text
    else:
        return "I'm sorry, I couldn't generate a response. Please try again."

# Initialize Streamlit app
st.set_page_config(page_title="Mental Health Chatbot")
st.header("Mental Health Chatbot")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Display chat history
if st.session_state['chat_history']:
    st.subheader("Chat History:")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

# Initialize emotion detection pipeline
emotion_classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion", return_all_scores=True)

# Function to detect emotion
def detect_emotion(text):
    emotions = emotion_classifier(text)
    emotions = emotions[0]
    # Sort by score
    emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)
    top_emotions = emotions[:2]  # Get the top 2 emotions
    # Print emotions to terminal
    print("Detected Emotions:")
    for emotion in top_emotions:
        print(f"{emotion['label']}: {emotion['score']:.2f}")
    return top_emotions

# Function to record voice input
def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.write(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        st.write("Could not request results; check your network connection.")
        return ""

# Function to play audio from text using pyttsx3 with voice selection
def play_audio(text, voice_id=None):
    engine = pyttsx3.init()

    # Change voice if voice_id is provided
    if voice_id:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[voice_id].id)

    engine.say(text)
    engine.runAndWait()

# Text input and voice interaction section
st.subheader("Chat with the Health Bot")
if not st.session_state['chat_history']:
    st.write("Hey there, how are you doing today?")

# Voice input button
if st.button("Speak"):
    input_text = record_voice()
    if input_text:
        emotions = detect_emotion(input_text)
        response_text = get_gemini_response(input_text, st.session_state['chat_history'], emotions)
        st.session_state['chat_history'].append(("You", input_text))
        st.subheader("The Response is")
        st.write(response_text)
        play_audio(response_text, voice_id=1)
        st.session_state['chat_history'].append(("Bot", response_text))

# Text input
input_text = st.text_input("Enter your message: ", key="input")
submit = st.button("Submit")

if submit and input_text:
    emotions = detect_emotion(input_text)
    response_text = get_gemini_response(input_text, st.session_state['chat_history'], emotions)
    st.session_state['chat_history'].append(("You", input_text))
    st.subheader("Health Bot's Response:")
    st.write(response_text)
    st.session_state['chat_history'].append(("Bot", response_text))
