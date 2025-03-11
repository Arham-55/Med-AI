import os
from flask import Flask, render_template, request, jsonify, session
from app import get_response  

os.environ["TOGETHER_API_KEY"] = "b586af6253ec4e6b9f18700893e9af1a523a01d43b4a4a59424c1d14f9b68329"

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/")
def home():
    return render_template("home.html")  # New homepage

@app.route("/chatbot")
def chatbot():
    session.clear()  # Clear session when opening chatbot
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    if "history" not in session:
        session["history"] = []

    session["history"].append(f"You: {user_message}")

    full_conversation = "\n".join(session["history"])
    bot_reply = get_response(full_conversation)

    session["history"].append(f"Bot: {bot_reply}")

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
