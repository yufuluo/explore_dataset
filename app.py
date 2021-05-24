import logging
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

from api.get_column_distinct import get_column_distinct
from api.analyze_data import analyze_data

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_db_connection():
    conn = sqlite3.connect('./db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_column_distinct')
def get_column_distinct_handler():
    column_name = request.args.get('column_name')
    return get_column_distinct({'column_name': column_name})

@app.route('/api/analyze_data', methods=['POST'])
def find_total_viewers():
    data = request.get_json()
    cities = data.get('cities', [])
    metrics = data.get('metrics', 'total_viewers')
    group_by = data.get('group_by', 'genre')
    return analyze_data({'metrics': metrics, 'group_by': group_by, 'filter': {'city': cities}})
