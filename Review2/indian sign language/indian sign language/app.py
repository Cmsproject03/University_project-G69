from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import os
import logging

app = Flask(__name__)

# Initialize the recognizer
r = sr.Recognizer()

isl_gif = [
    'any_questions', 'are_you_angry', 'are_you_busy', 'are_you_hungry', 'are_you_sick',
    # Add more items as needed
]

arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voice_input', methods=['POST'])
def voice_input():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        logging.debug("I am Listening")  # Log that the app is listening
        audio = r.listen(source)
        
        try:
            speech = r.recognize_google(audio).lower()  # Recognize speech from audio input
            logging.debug(f"You Said: {speech}")  # Log the speech input
            
            # Process the speech input
            if speech in isl_gif:
                response = {"type": "gif", "gif_name": f"{speech}.gif"}
            else:
                images = []
                for char in speech:
                    if char in arr:
                        image_path = f'static/letters/{char}.jpg'
                        if os.path.exists(image_path):
                            images.append(image_path)
                response = {"type": "images", "images": images}

            return jsonify(response)
        except Exception as e:
            logging.error(f"Error: {e}")  # Log the error
            return jsonify({"error": f"Sorry, I couldn't understand the speech. Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
