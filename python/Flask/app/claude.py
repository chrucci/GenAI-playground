from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
)
from litellm import completion
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for sessions
app.permanent_session_lifetime = timedelta(days=5)  # Set session lifetime

# List of available LLMs
LLMS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-32k",
    "gpt-4o",
    "claude-3-haiku-20240307",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-5-sonnet-20240620",
    "ollama/codellama",
    "ollama/mistral",
    "ollama/mixtral",
    "ollama/llama2",
    "ollama/llama3",
]


@app.route("/", methods=["GET", "POST"])
def index():
    if "conversation" not in session:
        session["conversation"] = []

    if request.method == "POST":
        selected_llm = request.form["llm"]
        prompt = request.form["prompt"]

        session["conversation"].append({"role": "user", "content": prompt})

        try:
            response = completion(model=selected_llm, messages=session["conversation"])
            response_content = response["choices"][0]["message"]["content"]
            session["conversation"].append(
                {"role": "assistant", "content": response_content}
            )
            session.modified = True
            return jsonify({"status": "success", "response": response_content})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    return render_template(
        "index.html", llms=LLMS, conversation=session["conversation"]
    )


@app.route("/reset", methods=["POST"])
def reset():
    session["conversation"] = []
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
