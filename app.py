from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from sqlalchemy import create_engine, text
from datetime import datetime

app = Flask(__name__)

engine = create_engine('sqlite:///database.db')
connection = engine.connect()


@app.route('/')
def home():
    query = text('SELECT * FROM logs')
    result = connection.execute(query).fetchall()

    return render_template('home.html', logs=result)



@app.route('/add_log', methods=['GET'])
def show_form():
    return render_template('add_log.html')


app.run(debug=True, reloader_type='stat', port=5000)

