import wikipedia
import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
import tkinter as tk
from tkinter import scrolledtext
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 175)

class LuminaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌌 Lumina AI Assistant")
        self.root.geometry("880x540")
        self.root.configure(bg="#1e1e2f")
        self.create_widgets()
        self.speak("I'm Lumina, ready to assist you.")

    def speak(self, text):
        self.chat_history.insert(tk.END, f"\n🧠 Lumina: {text}\n", "lumina")
        self.chat_history.yview(tk.END)
        engine.say(text)
        engine.runAndWait()

    def wish_user(self):
        hour = datetime.datetime.now().hour
        if hour < 12:
            self.speak("Good morning, my creator!")
        elif hour < 18:
            self.speak("Good afternoon!")
        else:
            self.speak("Good evening!")

    def create_widgets(self):
        style = {"bg": "#1e1e2f", "fg": "#f8f8f2", "font": ("Consolas", 11)}

        self.chat_history = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=25, **style, insertbackground='white', borderwidth=0)
        self.chat_history.grid(row=0, column=1, padx=10, pady=10)
        self.chat_history.tag_config("lumina", foreground="#89ddff")
        self.chat_history.tag_config("user", foreground="#c3e88d")

        self.history_list = tk.Listbox(self.root, width=30, bg="#292942", fg="#ffffff", font=("Consolas", 10), highlightthickness=0, selectbackground="#44475a")
        self.history_list.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="ns")

        self.entry = tk.Entry(self.root, width=68, bg="#2e2e3d", fg="#ffffff", insertbackground="white", font=("Consolas", 11), relief=tk.FLAT)
        self.entry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="w")
        self.entry.bind("<Return>", self.on_enter)

        self.voice_button = tk.Button(self.root, text="🎤", font=("Arial", 12), bg="#89ddff", fg="#1e1e2f", width=4, relief=tk.FLAT, command=self.start_listening)
        self.voice_button.grid(row=1, column=1, sticky="e", padx=10, pady=(0, 10))

    def on_enter(self, event):
        query = self.entry.get()
        self.entry.delete(0, tk.END)
        self.chat_history.insert(tk.END, f"\n🗣️ You: {query}\n", "user")
        self.history_list.insert(tk.END, f"🗣️ {query[:30]}")
        self.process_query(query.lower())

    def start_listening(self):
        threading.Thread(target=self.take_command).start()

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("Listening...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)

        try:
            query = r.recognize_google(audio, language='en-US')
            self.chat_history.insert(tk.END, f"\n🗣️ You (voice): {query}\n", "user")
            self.history_list.insert(tk.END, f"🎤 {query[:30]}")
            self.process_query(query.lower())
        except:
            self.speak("Sorry, I didn’t catch that.")

    def process_query(self, query):
        if "youtube" in query:
            self.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif "google" in query:
            self.speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        elif "notepad" in query:
            self.speak("Opening Notepad.")
            os.system("notepad")

        elif "time" in query:
            time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {time}")

        elif "exit" in query or "quit" in query or "close" in query:
            self.speak("Goodbye! I'm always here if you need me.")
            self.root.quit()

        elif "video" in query:
            self.speak("Opening your videos folder.")
            os.startfile("C:\\Users\\Syed Shabbir\\Videos")

        elif "music" in query or "song" in query:
            self.speak("Opening your music folder.")
            os.startfile("C:\\Users\\Syed Shabbir\\Music")

        elif "code" in query or "vs code" in query:
            self.speak("Opening Visual Studio Code.")
            os.startfile("C:\\Users\\Syed Shabbir\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")

        elif "photo" in query or "picture" in query:
            self.speak("Opening your pictures folder.")
            os.startfile("C:\\Users\\Syed Shabbir\\Pictures")

        elif "who is" in query or "what is" in query or "tell me about" in query:
            self.speak("Let me search that for you.")
            try:
                result = wikipedia.summary(query, sentences=2)
                self.speak(result)
            except:
                self.speak("Sorry, I couldn't find anything.")

        else:
            self.speak("Sorry, I didn’t catch that. But I'm learning every day!")

if __name__ == "__main__":
    root = tk.Tk()
    app = LuminaGUI(root)
    app.wish_user()
    root.mainloop()
