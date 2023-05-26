from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# API
@app.route("/api")
def api():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
