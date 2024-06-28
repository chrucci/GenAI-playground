# app.py
from flask import Flask, render_template, request, Response, stream_with_context
from litellm import completion
import os

app = Flask(__name__)

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
]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_llm = request.form["llm"]
        prompt = request.form["prompt"]

        def generate():
            try:
                for chunk in completion(
                    model=selected_llm,
                    messages=[{"role": "user", "content": prompt}],
                    stream=True,
                ):
                    content = chunk["choices"][0]["delta"].get("content", "")
                    if content:
                        yield content.encode("utf-8")
            except Exception as e:
                yield str(e).encode("utf-8")

        return Response(
            stream_with_context(generate()), content_type="text/plain; charset=utf-8"
        )

    return render_template("index.html", llms=LLMS)


if __name__ == "__main__":
    app.run(debug=True)
