# Gemini Chatbot Implementation with Web Interface
# This script creates a web-based chatbot using Google's Gemini API

import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

class GeminiChatbot:
    def __init__(self):
        self.history = []
        self.configure_api()
        
    def configure_api(self):
        """Configure the Gemini API with the API key from environment."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("No API key found. Please set GEMINI_API_KEY in .env file.")
        
        try:
            genai.configure(api_key=api_key)
            
            # Initialize the model with the latest Gemini version
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            self.chat = self.model.start_chat(history=[])
            print("Successfully initialized Gemini 1.5 Pro model")
        except Exception as e:
            print(f"Error during API configuration: {str(e)}")
            raise
        
    def send_message(self, message):
        """Send a message to the model and get a response."""
        try:
            response = self.chat.send_message(message)
            if hasattr(response, 'text'):
                self.history.append({"role": "user", "parts": [message]})
                self.history.append({"role": "model", "parts": [response.text]})
                return response.text
            else:
                return "Sorry, I couldn't generate a response at the moment."
        except Exception as e:
            print(f"Error in send_message: {str(e)}")
            return f"Error: {str(e)}"

# Create a global chatbot instance
chatbot = GeminiChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = chatbot.send_message(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5004)
    