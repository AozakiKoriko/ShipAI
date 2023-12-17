from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from manifest_import import parse_cargo_info
from grid_creator import fill_grid_with_cargos


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'sdssds5057')


# setting upload path
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('main_page.html')  

@app.route('/submit-target-list', methods=['POST'])
def submit_target_list():
    data = request.get_json()
    target_list = [tuple(item) for item in data.get('targetList', [])]
    print("Received target_list: ",target_list)
    return jsonify({"status": "success"})

@app.route('/get-grid')
def get_grid():
    grid = session.get('grid',[])
    return jsonify(grid)

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


if __name__ == '__main__':
    app.run(debug=True)

