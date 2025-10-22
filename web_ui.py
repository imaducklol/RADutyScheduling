from flask import Flask, request, render_template, jsonify
import scheduler

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['data']
        result = process_input(user_input)
        return f"Result: {result}"
    return (
"""
<div style="max-width: 500px; margin: auto; font-family: sans-serif;">
    <form method="POST">
        <p>
            On each line, enter a person's name followed by their ranked
            preferences for days of the week, separated by commas. 
            <br><br>
            Example:<br>
            Alice, Monday, Wednesday, Sunday, Thursday, Tuesday<br>
            Bob, Tuesday, Thursday, Sunday, Wednesday, Monday<br>
        </p>

        <textarea name="data" 
                style="width: 100%; font-size: 16px; padding: 8px; 
                margin-bottom: 12px; resize: none; overflow: hidden;"
                oninput="this.style.height='auto'; 
                this.style.height=this.scrollHeight+'px'"></textarea>
        
        <input type="submit" 
            style="font-size: 16px; padding: 8px 16px; cursor: pointer;"/>
    </form>
</div>
""")

def process_input(user_input):
    print(user_input)
    return user_input

if __name__ == '__main__':
    app.run(debug=True)