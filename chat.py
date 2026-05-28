from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")  # FIX: was "templates.html", Flask looks inside /templates folder automatically

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_question = data.get("message", "")

        if user_question.strip() == "":
            return jsonify({"reply": "Please type a question."})

        response = client.models.generate_content(
            model="gemini-2.5-flash",  # FIX: "gemini-3.5-flash" does not exist, use gemini-2.0-flash
            contents=user_question
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(debug=True)