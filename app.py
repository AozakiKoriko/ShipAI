from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from manifest_import import parse_cargo_info
from grid_creator import fill_grid_with_cargos
from onload_offload_main import onload_offload_algorithm
import json
from datetime import datetime
from balance import run


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'sdssds5057')


# setting upload path
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
LOG_FOLDER = os.path.join(BASE_DIR, 'log')
app.config['LOG_FOLDER'] = LOG_FOLDER

def log_action(action):
    try:
        current_time = datetime.now().strftime("%B %d %Y: %H:%M")
        log_message = f"{current_time} {action}\n"

        log_file_path = os.path.join(app.config['LOG_FOLDER'], 'log.txt')
        with open(log_file_path, 'a') as file:
            file.write(log_message)
    except Exception as e:
        print(f"Error writing to log file: {e}")

@app.route('/')
def index():
    return render_template('main_page.html')  

@app.route('/report', methods=['POST'])
def report():
    data = request.json
    report = data.get('report', '')
    log_action(f"\"{report}\"")
    return jsonify({"status": "success", "message": "Report received."})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', 'Unknown')
    log_action(f"{username} signs in")
    return jsonify({"status": "success", "message": f"Logged in as {username}"})

@app.route('/complete-action', methods=['POST'])
def complete_action():
    filename = session.get('filename', None)
    if filename:
        log_action(f"Finished a Cycle. Manifest {filename} was updated, and a reminder pop-up to operator to send file was displayed")
    print("Complete action triggered")
    return jsonify({"status": "success", "message": "Action completed successfully"})


@app.route('/submit-target-list', methods=['POST'])
def submit_target_list():
    data = request.get_json()
    target_list = [tuple(item) for item in data.get('targetList', [])]
    print("Received target_list: ",target_list)
    session['target_list'] = target_list
    return jsonify({"status": "success"})

@app.route('/submit-onload-list', methods=['POST'])
def submit_onload_list():
    data = request.get_json()
    onload_list = data.get('onloadList', [])
    weight_list = data.get('weightList', [])
    filepath = session.get('filepath')
    print("Using filepath:",filepath)
    target_list = session.get('target_list', [])
    print("Using target_list: ",target_list)
    onload_offload_algorithm(filepath, target_list, onload_list, weight_list) 
    return jsonify({"status": "success"})


@app.route('/get-steps')
def get_steps():
    try:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'output.json'), 'r') as file:
            data = json.load(file)
            return jsonify(data)
    except IOError:
        return jsonify({"error": "File not found"}), 404

@app.route('/get-grid')
def get_grid():
    grid = session.get('grid',[])
    return jsonify(grid)

@app.route('/step-page')
def step_page():
    return render_template('step_page.html')

@app.route('/balance-process-page')
def balance_process_page():
    return render_template('balance_process_page.html')

@app.route('/process-page')
def process_page():
    return render_template('process_page.html')

@app.route('/onload-page')
def onload_page():
    return render_template('onload_page.html')

@app.route('/offload-page')
def offload_page():
    return render_template('offload_page.html')

@app.route('/onload-offload', methods=['POST'])
def onload_offload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        cargos = parse_cargo_info(filepath)
        grid = fill_grid_with_cargos(cargos)
        session['grid'] = grid
        session['filepath'] = filepath
        session['filename'] = filename
        string_count = sum(isinstance(item, str) for row in grid for item in row)
        log_action(f"{filename} is opened, there are {string_count} containers on the ship")
        return redirect(url_for('offload_page'))


@app.route('/balance', methods=['POST'])
def balance():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        cargos = parse_cargo_info(filepath)
        grid = fill_grid_with_cargos(cargos)
        session['grid'] = grid
        string_count = sum(isinstance(item, str) for row in grid for item in row)
        log_action(f"{filename} is opened, there are {string_count} containers on the ship") 
        run(filepath)
        return redirect(url_for('balance_process_page'))



if __name__ == '__main__':
    app.run(debug=True)

