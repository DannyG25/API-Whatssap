from flask import Flask
from flask import render_template
from flask import request



app = Flask(__name__)

@app.route("/")
def home():
  return "Hello world!"
  
if __name__ == "__main__":
  app.run()