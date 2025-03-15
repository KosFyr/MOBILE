import flask
import google.generativeai as genai
import os

app = flask.Flask(__name__)

# Φόρτωση API Key από το περιβάλλον
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

@app.route("/", methods=["GET"])
def home():
    return "AI Voice Assistant Server is Running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = flask.request.json
    user_message = data.get("message", "")

    if not user_message:
        return flask.jsonify({"error": "No message provided"}), 400

    try:
        model = genai.GenerativeModel("gemini-pro")  # Χρησιμοποιούμε το Gemini AI
        response = model.generate_content(user_message)
        ai_response = response.text if response.text else "Συγγνώμη, δεν κατάλαβα."

        return flask.jsonify({"response": ai_response})

    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
