import flask
import google.generativeai as genai
import os

app = flask.Flask(__name__)

# Φόρτωση API Key από το περιβάλλον
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

@app.route("/", methods=["GET"])
def home():
    return "AI Voice Assistant Server is Running!"  # Αντικατάσταση του μηνύματος

@app.route("/chat", methods=["POST"])
def chat():
    # Εξαγωγή δεδομένων από το αίτημα
    data = flask.request.json
    user_message = data.get("message", "")

    # Εκτύπωση για debugging
    print(f"Received message: {user_message}")

    # Αν δεν υπάρχει μήνυμα, επιστρέφουμε λάθος
    if not user_message:
        return flask.jsonify({"error": "No message provided"}), 400

    try:
        # Χρησιμοποιούμε το μοντέλο Gemini AI
        model = genai.GenerativeModel("gemini-2.0")  # Χρησιμοποιούμε το σωστό μοντέλο
        response = model.generate_content(user_message)
        ai_response = response.text if response.text else "Συγγνώμη, δεν κατάλαβα."

        # Εκτύπωση για debugging
        print(f"AI response: {ai_response}")

        return flask.jsonify({"response": ai_response})  # Επιστροφή της απάντησης από το AI

    except Exception as e:
        # Εκτύπωση του σφάλματος για debugging
        print(f"Error: {str(e)}")
        return flask.jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
