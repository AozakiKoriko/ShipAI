from flask import Flask, request, redirect, session, url_for,render_template,jsonify
import log_file
import logging
import os
import grid_creator
from manifest_import import parse_cargo_info
import json
app = Flask(__name__)
app.logger.setLevel(logging.ERROR)
app.secret_key = 'a1b2c3d4e5f6g7h8i9j0k_qwerty_12345!@#$%'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    log_file.log_login(username)
    session['username'] = username
    return redirect(url_for('static', filename='import.html'))

@app.route('/newLogin', methods=['POST'])
def new_login():
    data = request.json
    username = data['username']
    log_file.log_login(username)  
    session['username'] = username
    return jsonify({"message": "Username logged successfully."})

@app.route('/FacePage')
def face_page():
    return render_template('FacePage.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join('manifest_dir', file.filename)
            file.save(filepath)
            cargos = parse_cargo_info(filepath)
            grid = grid_creator.create_grid_from_manifest(filepath)
            session['array_result'] = grid  
            grid_json = json.dumps(grid) 
            return render_template('options.html', username=session.get('username'), array_result=grid_json)
    except Exception as e:
        print("An error occured:", e)  
           
@app.route('/options')
def options():
    return render_template('options.html', username=session.get('username'))
  
    
@app.route('/load_and_unload')
def load_and_unload():
    grid_json = json.dumps(session.get('array_result', [])) 
    return render_template('load_and_unload.html', username=session.get('username'), array_result=grid_json)

@app.route('/balance')
def balance():
    grid_json = json.dumps(session.get('array_result', [])) 
    return render_template('balance.html', username=session.get('username'), array_result=grid_json)

@app.route('/log_message', methods=['POST'])
def log_message():
    try:
        data = request.json
        username = data.get('username')
        message = data.get('message')

        # Log the username and message using log_user_message
        log_file.log_user_message(username, message)

        return json.dumps({'status': 'success'})
    except Exception as e:
        print("An error occurred:", e)
        return json.dumps({'status': 'error', 'message': str(e)})

@app.route('/save-containers', methods=['POST'])
def save_containers():
    data = request.json
    selected_containers = data.get('selectedContainers', [])
    loaded_containers = data.get('loadedContainers', [])

    # Process and save data here
    # For example, saving to a file
    with open('containers_data.json', 'w') as file:
        json.dump(data, file, indent=4)

    return jsonify({"message": "Containers data saved successfully"})

if __name__ == '__main__':
    app.run(debug=True)