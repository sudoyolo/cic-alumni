from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
   return render_template('index.html')

@app.route('/SignIn')
def SignIn_page():
   return render_template('login.html')

@app.route('/SearchAlumni')
def Seacrh_alumni():
   return render_template('index.html')