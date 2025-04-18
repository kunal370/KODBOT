from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Add this right after app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Add this check in app.py before genai.configure()
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("Missing GEMINI_API_KEY in .env file")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_code():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug log

        if not data:
            return jsonify({"error": "No data received"}), 400

        prompt = data.get('prompt')
        language = data.get('language', 'Python')

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(
            f"Generate {language} code for: {prompt}. Provide only the code with comments."
        )

        print("Generated response:", response.text)  # Debug log
        return jsonify({"code": response.text})

    except Exception as e:
        print("Error:", str(e))  # Debug log
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


