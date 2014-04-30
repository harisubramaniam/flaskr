import os
from flask import Flask, render_template, request, url_for

# Initialization
app = Flask(__name__)
app.config.update(
	DEBUG = True,
)

# Controllers
@app.route("/")
def hello():
	return "Hello from Python!"


# Launch
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="localhost", port=port)