import os
from flask import Flask, request, render_template, jsonify
from app.scheduler import Scheduler

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            scheduler = Scheduler()
            dict_input: dict = {}

            for line in request.form['data'].splitlines():
                parts = [part.strip() for part in line.split(',')]
                name = parts[0]
                preferences = parts[1:]
                dict_input[name] = preferences
            
            scheduler.load_dict(dict_input)

            result = scheduler.run()
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
    
    return app