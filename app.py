from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import threading
import os
import sys
import webbrowser
import time

print("--- SYSTEM BOOT ---")
print("1. Loading Modules...")

try:
    import jarvis_core as jarvis
    print("2. Core Loaded.")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Windows Friendly Settings
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

state = {'is_active': False}

def run_assistant_logic():
    print("Background Thread Started")
    # Small delay to ensure UI is ready
    time.sleep(1)
    jarvis.speak("System Online")
    socketio.emit('status', {'text': 'ONLINE'})
    
    while state['is_active']:
        try:
            socketio.emit('status', {'text': 'LISTENING...'})
            query = jarvis.command().lower()
            
            if query == "none": continue

            socketio.emit('message', {'role': 'user', 'text': query})
            socketio.emit('status', {'text': 'PROCESSING...'})

            if "whatsapp" in query and "send" in query:
                response = jarvis.handle_whatsapp_logic(query)
            elif (sys_resp := jarvis.execute_system_command(query)):
                response = sys_resp
            else:
                response = jarvis.ask_llm(query)

            jarvis.speak(response)
            socketio.emit('message', {'role': 'jarvis', 'text': response})
            
        except Exception as e:
            print(f"Loop Error: {e}")
            socketio.emit('status', {'text': 'ERROR'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def stats():
    return jsonify(jarvis.get_system_stats())

@socketio.on('toggle_jarvis')
def handle_toggle(data):
    if data['status'] == 'start':
        if not state['is_active']:
            state['is_active'] = True
            threading.Thread(target=run_assistant_logic, daemon=True).start()
    else:
        state['is_active'] = False
        socketio.emit('status', {'text': 'OFFLINE'})

if __name__ == '__main__':
    port = 5050
    url = f"http://127.0.0.1:{port}"
    print(f"3. Starting Server at {url}")
    print("Check your browser now!")
    
    # Auto-open browser
    threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    
    # Run server
    socketio.run(app, debug=True, port=port, allow_unsafe_werkzeug=True, use_reloader=False)