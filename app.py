from flask import Flask, request, render_template, redirect, url_for, session
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import io
import base64
from datetime import timedelta

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
app.secret_key = '0f3a39e26d4c8bd48bc8bad6466f488e155845889fdefbe568e11935f16a591e'
app.permanent_session_lifetime = timedelta(minutes=30)

# --- VISION CHATBOT ---
@app.route('/vision', methods=['GET', 'POST'])
def vision_chat():
    if 'chat_history' not in session:
        session['chat_history'] = []

    chat_history = session['chat_history']
    prompt = ""
    image_data = None

    if request.method == 'POST':
        prompt = request.form.get('prompt', '')
        file = request.files.get('image')

        if file:
            image_bytes = file.read()
            image_data = base64.b64encode(image_bytes).decode('utf-8')
            image = Image.open(io.BytesIO(image_bytes))

            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([prompt, image]).text

            # Save conversation
            chat_history.append({
                'prompt': prompt,
                'image': image_data,
                'response': response
            })
            session['chat_history'] = chat_history

    return render_template("vision.html", chat_history=chat_history)

# --- HOME PAGE ---
@app.route('/')
def index():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
