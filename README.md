# JARVIS 🤖
### An AI-Powered Voice Assistant with Web Interface

---

## 📋 Overview

JARVIS is an intelligent voice assistant built with **Google Gemini AI** that can understand your commands, send WhatsApp messages, open applications, play music, search the web, and have natural conversations. It features a web-based interface with real-time status updates and message history.
<img width="1901" height="903" alt="image" src="https://github.com/user-attachments/assets/d5ae3fb4-8e16-43ef-b2c4-9089d4762ebe" />


---

## 🚀 Features

✅ **Voice Recognition** - Listen to your commands in English (India accent)  
✅ **AI Chat** - Talk to Google Gemini AI for answers and conversations  
✅ **WhatsApp Integration** - Send messages to saved contacts via voice command  
✅ **System Automation** - Open apps, search Google, play YouTube videos  
✅ **Web Dashboard** - Real-time interface with status and chat history  
✅ **System Monitoring** - Check CPU usage and battery percentage  
✅ **Text-to-Speech** - Natural voice responses with adjustable speed  

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- Windows OS (for some features like notepad.exe)
- Microphone for voice input
- Internet connection

### Step 1: Clone/Download Project
```bash
cd JARVIS\ 2.0
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Or manually install:**
```bash
pip install flask flask-socketio python-socketio python-engineio pyttsx3 SpeechRecognition pyaudio google-generativeai python-dotenv pywhatkit psutil pyautogui
```

### Step 3: Setup API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key
3. Create a `.env` file in your project root:

```
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

⚠️ **Never commit `.env` to Git!** Add it to `.gitignore`:
```
.env
```

### Step 4: Configure Contacts

Edit `jarvis_core.py` and update the `CONTACTS` dictionary:

```python
CONTACTS = {
    "krish": "+919876543210", 
    "papa": "+919988776655",
    "mom": "+918877665544",
    "your_name": "+91XXXXXXXXXX"
}
```

---

## 🎮 How to Run

### Start JARVIS:
```bash
python app.py
```

This will:
1. ✔️ Load the AI model
2. ✔️ Start the Flask server on `http://127.0.0.1:5050`
3. ✔️ Auto-open your browser
4. ✔️ Initialize the voice assistant

---

## 📱 Voice Commands

### WhatsApp
```
"Send a message to krish saying hello"
"Message mom I am coming home"
"WhatsApp papa thank you"
```

### System Commands
```
"Open notepad"
"Open calculator"
"Google how to code in Python"
"Search YouTube"
"Play despacito on youtube"
```

### General Chat
```
"What is the capital of India?"
"Tell me a joke"
"How is the weather today?"
"What time is it?"
```

---

## 📂 Project Structure

```
JARVIS 2.0/
├── app.py                 # Flask server & web interface
├── jarvis_core.py         # AI logic, voice, WhatsApp
├── .env                   # API Key (DO NOT COMMIT)
├── .gitignore            # Git ignore rules
├── templates/
│   └── index.html        # Web dashboard UI
├── static/
│   ├── css/             # Styling
│   └── js/              # Frontend logic
└── README.md            # This file
```

---

## ⚙️ Configuration

### Change Voice Speed
In `jarvis_core.py`:
```python
engine.setProperty('rate', 170)  # Default: 170, Increase for faster
```

### Change AI Model
```python
CURRENT_MODEL_NAME = "models/gemini-1.5-flash"
```

### Adjust Listening Timeout
```python
audio = r.listen(source, timeout=5, phrase_time_limit=8)
# timeout: max wait time for speech
# phrase_time_limit: max duration of phrase
```

---

## 🔧 Troubleshooting

### ❌ "GEMINI_API_KEY not found"
- Check if `.env` file exists in project root
- Verify correct variable name: `GEMINI_API_KEY=...`
- Restart the application

### ❌ Microphone not working
```bash
pip install --upgrade pyaudio
# Windows: May need to install PortAudio first
```

### ❌ WhatsApp send fails
- Verify contact number format: `+91XXXXXXXXXX`
- Check internet connection
- Contact name must be in CONTACTS dictionary

### ❌ API Key quota exceeded
- Wait a few minutes
- Upgrade your Google AI Studio plan
- Check API usage at [aistudio.google.com](https://aistudio.google.com)

### ❌ Speech recognition keeps returning "None"
- Ensure microphone is working: `recorder -l`
- Speak clearly in English (Indian accent works)
- Check ambient noise levels

---

## 🔐 Security

⚠️ **Important Security Tips:**

1. **Never share your `.env` file**
2. **Never commit API key to GitHub**
3. **Keep `.gitignore` updated:**
   ```
   .env
   *.pyc
   __pycache__/
   .DS_Store
   ```
4. **Rotate API key regularly** if exposed
5. **Use environment variables** in production

---

## 🎯 Future Enhancements

   Multi-language support
   Custom voice profiles
   Email integration
   Calendar management
   Weather API integration
   Offline mode
   Docker containerization

---

## 📝 License

This project is open source. Feel free to modify and use!

---


## 👨‍💻 Built With

- **Google Gemini AI** - Intelligence
- **Flask & Flask-SocketIO** - Web framework
- **pyttsx3** - Text-to-speech
- **SpeechRecognition** - Voice input
- **pywhatkit** - WhatsApp automation
- **Python** - Backend

---

**Made with ❤️ | Version 2.0**
