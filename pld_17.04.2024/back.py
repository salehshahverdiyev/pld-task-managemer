from flask import Flask, render_template, request, redirect, jsonify
import json

app = Flask(__name__)

# Define the path to the JSON file
JSON_FILE = 'tasks.json'

def load_tasks():
    try:
        with open(JSON_FILE, 'r') as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []
    return tasks

def save_tasks(tasks):
    with open(JSON_FILE, 'w') as f:
        json.dump(tasks, f)

@app.route("/todo", strict_slashes=False)
def hello_world():
    tasks = load_tasks()
    return render_template("front.html", tasks=tasks)

@app.route('/todo-post', methods=['POST'])
def post_example():
    if request.method == 'POST':
        input_data = request.form['input']
        tasks = load_tasks()
        tasks.append(input_data)
        save_tasks(tasks)
        return redirect("/todo")

@app.route('/todo-delete/<int:index>', methods=['POST', 'DELETE'])
def delete_task(index):
    if request.method in ['POST', 'DELETE']:
        tasks = load_tasks()
        if 0 <= index < len(tasks):
            del tasks[index]
            save_tasks(tasks)
            return redirect("/todo")
    return jsonify({'error': 'Invalid index'}), 400


if __name__ == '__main__':
    app.run(debug=True)