from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
)
from litellm import completion
from langfuse import Langfuse
import os
from datetime import timedelta
import uuid
import sys

sys.path.append("../..")

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for sessions
app.permanent_session_lifetime = timedelta(days=5)  # Set session lifetime

# Initialize Langfuse
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv(
        "LANGFUSE_HOST", "https://cloud.langfuse.com"
    ),  # Optional, use "https://cloud.langfuse.com" for Langfuse Cloud
)

# List of available LLMs
LLMS = [
    "gpt-3.5-turbo",
    "gpt-4",
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


# Predefined prompts
PROMPTS = [
    {"name": "Extract Wisdom", "value": "Let's have a friendly conversation."},
    {"name": "Code Explanation", "value": "Explain the following code: "},
    {"name": "Text Summarization", "value": "Summarize the following text: "},
    {"name": "Creative Writing", "value": "Write a short story about: "},
    {"name": "Problem Solving", "value": "How would you solve this problem: "},
]


@app.route("/", methods=["GET", "POST"])
def index():
    if "conversation" not in session:
        session["conversation"] = []
        session["trace_id"] = str(uuid.uuid4())

    if request.method == "POST":
        selected_llm = request.form["llm"]
        prompt = request.form["prompt"]

        # Get model parameters from the form
        temperature = float(request.form.get("temperature", 0.7))
        top_p = float(request.form.get("top_p", 1.0))
        max_tokens = int(request.form.get("max_tokens", 500))

        session["conversation"].append({"role": "user", "content": prompt})

        try:
            trace = langfuse.trace(
                id=session["trace_id"], metadata={"model": selected_llm}
            )

            trace.event(name="user_input", input=prompt)

            base_url = (
                os.getenv("OLLAMA_BASE_URL")
                if selected_llm.startswith("ollama")
                else None
            )
            generation = trace.generation(
                name="llm_call",
                model=selected_llm,
                model_parameters={
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_tokens": max_tokens,
                    "base_url": base_url,
                },
                input=session["conversation"],
                is_streamed=False,
            )

            response = completion(
                model=selected_llm,
                messages=session["conversation"],
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
            )
            response_content = response["choices"][0]["message"]["content"]

            generation.end(
                output=response_content,
                completion_tokens=response["usage"]["completion_tokens"],
                prompt_tokens=response["usage"]["prompt_tokens"],
                total_tokens=response["usage"]["total_tokens"],
            )

            session["conversation"].append(
                {"role": "assistant", "content": response_content}
            )
            session.modified = True

            return jsonify({"status": "success", "response": response_content})
        except Exception as e:
            trace = langfuse.trace(id=session["trace_id"])
            trace.event(level="ERROR", name="llm_error", input=str(e))
            return jsonify({"status": "error", "message": str(e)})

    return render_template(
        "index.html", llms=LLMS, prompts=PROMPTS, conversation=session["conversation"]
    )


@app.route("/reset", methods=["POST"])
def reset():
    session["conversation"] = []
    session["trace_id"] = str(uuid.uuid4())
    return "", 204


@app.route("/rate", methods=["POST"])
def rate():
    rating = request.json.get("rating")
    if rating is not None:
        trace = langfuse.trace(id=session["trace_id"])
        trace.score(name="user_rating", value=rating)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid rating"}), 400


if __name__ == "__main__":
    app.run(debug=True)
