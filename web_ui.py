from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['data']
        result = process_input(user_input)
        return f"Result: {result}"
    return """
        <form method="POST">
        <input type="text" name="data" />
        <input type="submit" />
        </form>"""

def process_input(user_input):
    print(user_input)