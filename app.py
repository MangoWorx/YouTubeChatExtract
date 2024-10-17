from flask import Flask, render_template, request, redirect, url_for
import threading
import subprocess
import time

app = Flask(__name__)

# Variable to hold the running process
process = None
process_lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_script():
    global process

    # Get URL from the form
    url = request.form['youtube_url']
    driver_path = r'C:\\Users\\richa\\Documents\\chromedriver-win64\\chromedriver.exe'

    # Start the script if not already running
    with process_lock:
        if process is None:
            command = [
                'python', 'youtube_chat_live_extraction_02_with_gui.py', url, driver_path
            ]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop_script():
    global process

    # Stop the script if it is running
    with process_lock:
        if process is not None:
            process.terminate()
            process = None
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
