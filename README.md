# Mental-Heath-Chatbot
# Mental Health Chatbot

## Overview
This project is a Mental Health Chatbot application built using Streamlit. The chatbot uses Google's Generative AI model (Gemini Pro) to provide empathetic responses, detect emotions from user input, and allow voice interaction. The primary goal of the chatbot is to simulate a therapy session, offering users a supportive and empathetic conversational partner.

## Features
- **Text and Voice Interaction**: Users can interact with the chatbot either through text input or voice input.
- **Empathetic Responses**: The chatbot is designed to provide empathetic responses based on the user's input.
- **Emotion Detection**: The chatbot detects emotions from the user's input and displays the top two detected emotions.
- **Voice Feedback**: The chatbot can respond with audio output using different voice options.

## Technology Stack
- **Python**: Programming language used for the development of the application.
- **Streamlit**: Framework used for building the web application.
- **Google Generative AI (Gemini Pro)**: Model used for generating chatbot responses.
- **SpeechRecognition**: Library used for capturing and converting voice input to text.
- **Pyttsx3**: Library used for converting text to speech.
- **Transformers**: Library used for emotion detection through pre-trained models.
- **Dotenv**: Library used for loading environment variables from a `.env` file.

## Prerequisites
- Python 3.7+
- Streamlit
- Google Generative AI access and API key
- Microphone for voice input

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required packages:
    ```bash
    pip install streamlit google-generativeai SpeechRecognition python-dotenv transformers pyttsx3
    ```

3. Set up your `.env` file with your Google API key:
    ```env
    GOOGLE_API_KEY=your_google_api_key
    ```

## Usage

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Open your browser and navigate to `http://localhost:8501` to interact with the chatbot.
