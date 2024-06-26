from flask import Flask, render_template, jsonify
from ref import get_llm_list

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/hello/<name>")
def hello_name(name):
    list = ["foo", "bar", "baz"]
    return render_template("hello.html", name=name, items=list)


@app.route("/update-items", methods=["GET"])
def update_items():
    # New list of items
    # new_items = ["apple", "orange", "banana"]
    new_items = get_llm_list()
    return jsonify(new_items)


if __name__ == "__main__":
    app.run(debug=True)
