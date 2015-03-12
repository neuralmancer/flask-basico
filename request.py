from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get("User-Agent")
    return "tu navegador es {0}".format(user_agent)


if __name__ == "__main__":
    app.debug = True
    app.run()
