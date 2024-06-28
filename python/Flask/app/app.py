from flask import Flask, render_template, jsonify, request
from ref import get_llm_list

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/hello/<name>")
def hello_name(name):
    list = get_llm_list()
    return render_template("hello.html", name=name, items=list)


@app.route("/submit-prompt", methods=["POST"])
def ajax_call():
    data = request.form.get("message")
    llm = request.form.get("llm")
    # Process the data and generate a response
    # response = process_data(data)
    return (
        "THIS IS what you sent: " + data + " and " + llm + " was the LLM you selected!"
    )


@app.route("/update-items", methods=["GET"])
def update_items():
    # New list of items
    # new_items = ["apple", "orange", "banana"]
    new_items = get_llm_list()
    return jsonify(new_items)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
