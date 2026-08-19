from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from sqlalchemy import create_engine, text
from datetime import datetime

app = Flask(__name__)

engine = create_engine('sqlite:///database.db')
connection = engine.connect()


@app.route('/')
def home():
    query = text('SELECT * FROM practice_logs')
    result = connection.execute(query).fetchall()

    print("LOGS FETCHED FROM DATABASE:", result)

    return render_template('home.html', logs=result)



@app.route('/add_log', methods=['GET', 'POST'])
def add_log():
    if request.method == 'POST':

        pieces = request.form.get('pieces_practiced')
        duration = request.form.get('duration_minutes')
        description = request.form.get('description')


        insert_query = text('''
            INSERT INTO practice_logs (pieces_practiced, duration_minutes, description) 
            VALUES (:pieces, :duration, :description)
        ''')

        with engine.begin() as connection:  
            connection.execute(insert_query, {
                'pieces': pieces,
                'duration': duration,
                'description': description
            })

       
        return redirect(url_for('home'))

    
    return render_template('add_log.html')
    


app.run(debug=True, reloader_type='stat', port=5001)

