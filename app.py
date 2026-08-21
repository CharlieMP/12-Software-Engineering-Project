import os
from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import create_engine, text
# Removed unused imports ('send_from_directory', 'datetime') to clean up memory footprint.

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database.db')
engine = create_engine(f'sqlite:///{db_path}', pool_pre_ping=True)

# query completion assisted by ai
WEEKLY_QUERY = text('''
    SELECT * FROM practice_logs 
    WHERE strftime('%Y-%W', created_at) = strftime('%Y-%W', 'now')
    ORDER BY created_at DESC
''')

ARCHIVE_QUERY = text('SELECT * FROM practice_logs ORDER BY created_at DESC')

INSERT_QUERY = text('''
    INSERT INTO practice_logs (pieces_practiced, duration_minutes, description) 
    VALUES (:pieces, :duration, :description)
''')


@app.route('/')
def home():
    with engine.connect() as connection:
        result = connection.execute(WEEKLY_QUERY).mappings().all()

    # Removed print() debug line to keep server terminal output clean in production
    return render_template('home.html', logs=result)


@app.route('/archive')
def archive():
    with engine.connect() as connection:
        result = connection.execute(ARCHIVE_QUERY).mappings().all()

    return render_template('archive.html', logs=result)


# had ai assistance in completing the add log route
@app.route('/add_log', methods=['GET', 'POST'])
def add_log():
    if request.method == 'POST':
        with engine.begin() as connection:  
            connection.execute(INSERT_QUERY, {
                'pieces': request.form.get('pieces_practiced'),
                'duration': request.form.get('duration_minutes'),
                'description': request.form.get('description')
            })

        return redirect(url_for('home'))

    return render_template('add_log.html')


if __name__ == '__main__':
    app.run(debug=True, reloader_type='stat', port=5001)
    # changed the port to 5001 to deal with a port error that i frequently encountered