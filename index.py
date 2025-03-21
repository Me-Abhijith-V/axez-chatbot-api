from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

app = Flask(__name__)



load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

messages = [{"role": "system", "content": "You are Axez, an educated assistant"}]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json["message"]
    messages.append({"role": "user", "content": user_message})

    try:
        output = openai.chat.completions.create(
            model="gpt-4o-mini",  # Or your preferred model
            messages=messages
        )
        bot_response = output.choices[0].message.content
        messages.append({"role": "assistant", "content": bot_response})
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)