from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2> Welcome to the Cool Flask App</h2>
    <p>Try these URLs:</p>
    <ul>
        <li>/uppercase?name=Omkar</li>
        <li>/reverse?name=Flask</li>
        <li>/length?name=Python</li>
        <li>/greet?name=Developer</li>
    </ul>
"""

@app.route("/uppercase")
def uppercase_name():
    name = request.args.get("name", "Guest")
    return f"<h1> Uppercase name: {name.upper()}<h1>"

@app.route("/reverse")
def reverse_name():
    name=request.args.get("name","Guest")
    return f"<h1> Reversed Name: {name[::-1]}<h1>"

@app.route("/length")
def name_length():
    name = request.args.get("name", "Guest")
    return f"<h1>Length of '{name}': {len(name)} characters</h1>"

@app.route("/greet")
def greet_user():
    name = request.args.get("name", "Guest")
    return f"""
    <h1>Hello, {name.upper()}!</h1>
    <p>Welcome to your personalized Flask app</p>
    """

if __name__=="__main__":
    app.run(debug=True)