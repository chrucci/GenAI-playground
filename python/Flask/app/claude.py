from flask import (
    Flask,
    render_template,
    request,
    Response,
    stream_with_context,
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

        def generate():
            yield f"Human: {prompt}\n\n".encode("utf-8")
            yield f"{selected_llm}: ".encode("utf-8")
            try:
                response_content = ""
                for chunk in completion(
                    model=selected_llm, messages=session["conversation"], stream=True
                ):
                    content = chunk["choices"][0]["delta"].get("content", "")
                    if content:
                        response_content += content
                        yield content.encode("utf-8")
                session["conversation"].append(
                    {"role": "assistant", "content": response_content}
                )
                session.modified = True
            except Exception as e:
                yield str(e).encode("utf-8")

        return Response(
            stream_with_context(generate()), content_type="text/plain; charset=utf-8"
        )

    return render_template(
        "index.html", llms=LLMS, conversation=session["conversation"]
    )


@app.route("/reset", methods=["POST"])
def reset():
    session["conversation"] = []
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
