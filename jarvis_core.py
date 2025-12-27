import os
import datetime
import webbrowser
import pyautogui
import pyttsx3
import speech_recognition as sr
import psutil
import google.generativeai as genai
from dotenv import load_dotenv
import pywhatkit
import json
import time

# --- WINDOWS THREAD FIX ---
try:
    import pythoncom
except ImportError:
    pythoncom = None

# --- CONFIGURATION & AUTO-MODEL SELECTOR ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Default Safe Model
CURRENT_MODEL_NAME = "models/gemini-1.5-flash"

print("--------------------------------------------------")
if not api_key:
    print("CRITICAL ERROR: 'GEMINI_API_KEY' not found!")
else:
    print(f"SUCCESS: API Key loaded (Starts with: {api_key[:4]}...)")
    genai.configure(api_key=api_key)
    
    # --- ROBUST MODEL DETECTION ---
    print("Scanning available AI models...")
    try:
        found_model = False
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        safe_priority = [
            'models/gemini-1.5-flash',
            'models/gemini-1.5-flash-001',
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-pro',
            'models/gemini-pro',
            'models/gemini-1.0-pro'
        ]
        
        for safe in safe_priority:
            if safe in all_models:
                CURRENT_MODEL_NAME = safe
                found_model = True
                break
        
        if not found_model:
            for m in all_models:
                if 'flash' in m and 'preview' not in m:
                    CURRENT_MODEL_NAME = m
                    found_model = True
                    break

        if found_model:
            print(f"✔ CONNECTED TO SAFE MODEL: {CURRENT_MODEL_NAME}")
        else:
            print(f"⚠ Could not find standard model. Forcing: {CURRENT_MODEL_NAME}")
            
    except Exception as e:
        print(f"⚠ Model Scan Failed (Using Default): {e}")

print("--------------------------------------------------")

# --- CONTACT LIST (Names must be lowercase) ---
CONTACTS = {
    "krish": "+919876543210", 
    "papa": "+919988776655",
    "mom": "+918877665544",
    "ritu": "+917065413389"
}

# --- AUDIO SETUP ---
def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    try:
        engine.setProperty('voice', voices[1].id)
    except:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)
    return engine

def speak(text):
    print(f"JARVIS: {text}")
    try:
        if pythoncom: pythoncom.CoInitialize()
        engine = initialize_engine()
        engine.say(text)
        engine.runAndWait()
        if pythoncom: pythoncom.CoUninitialize()
    except Exception as e:
        print(f"Speaker Error: {e}")

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Reduced adjust time to prevent long pauses
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("Listening...")
        try:
            # Increased timeout slightly
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "None"

# --- SMART AUTOMATION ---
def handle_whatsapp_logic(query):
    try:
        if not api_key: return "API Key missing."

        model = genai.GenerativeModel(CURRENT_MODEL_NAME)
        
        prompt = f"""
        Task: Extract recipient name and message from the query.
        Query: "{query}"
        Output: JSON only. No markdown.
        Format: {{"name": "name_here", "message": "message_here"}}
        """
        
        response = model.generate_content(prompt)
        cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(cleaned_text)
        
        # Strip removes extra spaces
        extracted_name = data.get("name").lower().strip()
        msg_content = data.get("message")
        
        print(f"DEBUG: Jarvis Extracted Name -> '{extracted_name}'")

        # SMART MATCHING LOGIC
        phone_no = None
        matched_name = None

        # Check exact or partial match
        for contact_key, number in CONTACTS.items():
            # Case 1: 'krish' == 'krish'
            if contact_key == extracted_name:
                phone_no = number
                matched_name = contact_key
                break
            # Case 2: 'krish' is inside 'krish sharma' (User said full name)
            elif contact_key in extracted_name:
                phone_no = number
                matched_name = contact_key
                break
        
        if phone_no:
            speak(f"Found contact {matched_name}. Sending message...")
            pywhatkit.sendwhatmsg_instantly(phone_no, msg_content, 25, True, 5)
            # Give system time to close browser and refocus
            time.sleep(2)
            return f"Message sent to {matched_name}. I am listening again."
        else:
            # Show user what names are available
            available_names = ", ".join(CONTACTS.keys())
            speak(f"I heard '{extracted_name}', but it's not in your list. Available contacts are: {available_names}")
            return f"Contact '{extracted_name}' not found."
            
    except Exception as e:
        print(f"WhatsApp Error: {e}")
        return "I encountered an error processing that request."

# --- SYSTEM COMMANDS ---
def execute_system_command(query):
    query = query.lower()
    
    # 1. Play Song on YouTube
    if "play" in query:
        song = query.replace("play", "").replace("on youtube", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
        return f"Playing {song} on YouTube"

    # 2. Open Apps
    elif "notepad" in query:
        os.startfile('notepad.exe')
        return "Opening Notepad"
    elif "calculator" in query:
        os.startfile('calc.exe')
        return "Opening Calculator"
    
    # 3. Browsing
    elif "google" in query:
        term = query.replace("google", "").replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={term}")
        return f"Searching Google for {term}"
    elif "youtube" in query:
        webbrowser.open("https://www.youtube.com/")
        return "Opening YouTube"
    
    return None

# --- LLM CHAT ---
def ask_llm(query):
    try:
        if not api_key:
            return "Please configure your API key."
            
        model = genai.GenerativeModel(CURRENT_MODEL_NAME)
        response = model.generate_content(f"You are Jarvis. Keep it short. User: {query}")
        return response.text
    except Exception as e:
        print(f"LLM CONNECTION ERROR: {e}")
        if "429" in str(e):
             return "My server is busy right now (Quota Exceeded). Please try again in a minute."
        return f"Offline Mode (Error: {str(e)[:20]}...)"

def get_system_stats():
    cpu = str(psutil.cpu_percent())
    battery = psutil.sensors_battery()
    bat_percent = battery.percent if battery else 100
    return {"cpu": cpu, "battery": bat_percent}