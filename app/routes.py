from flask import current_app as app

@app.route('/')
def home():
    return "Hello, World! This is the home page."

@app.route('/about')
def about():
    return "This is the about page."
