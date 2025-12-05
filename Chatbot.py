import os
from flask import Flask, request, jsonify, render_template
from cerebras.cloud.sdk import Cerebras
import webbrowser

app = Flask(__name__)

client = Cerebras(api_key="csk-hykry3ed95rx2xjk36p65mhvecm8n4hmd68kj36xmv2nxdt9")

@app.route("/")
def home():
    global chat_history
    chat_history = [
    {"role": "system", "content": "You are an avid Movie expert. Help me with finding the best movie based on my taste , ask me questions to clearify anything. Keep it short,I dont have time to read everything, be freindly. Once you've found the perfect movie for me, ask me first before you tell them ,and when you do, follow these rules: movie names and breif description only , no text formatting, no links ,no jargon, dont give me multiple options , help me pin point to 1 or at max 3."}
    ]

    return render_template("app.html")  # <-- loads your HTML page

chat_history = [
    {"role": "system", "content": "You are an avid Movie expert. Help me with finding the best movie based on my taste , ask me questions to clearify anything. Keep it short,I dont have time to read everything, be freindly. Once you've found the perfect movie for me, ask me first before you tell them ,and when you do, follow these rules: movie names and breif description only , no text formatting, no links ,no jargon, dont give me multiple options , help me pin point to 1 or at max 3."}
]

@app.route("/chat", methods=["POST"])
def chat():

    global chat_history


    data = request.get_json()
    user_msg = data.get("message", "")
    chat_history.append({"role": "user", "content": user_msg})

    completion = client.chat.completions.create(
        model="qwen-3-32b",
        messages=chat_history,
        max_completion_tokens=2048,
    )

    reply = completion.choices[0].message.content.split("</think>")[1][2:]
    #print(reply)

    chat_history.append({"role": "assistant", "content": reply})

    print('\n\n')
    print(chat_history)
    
    return jsonify({"reply": reply})

if __name__ == "__main__":
    #webbrowser.open("http://127.0.0.1:5050/")
    app.run(host="0.0.0.0",port="5050")
