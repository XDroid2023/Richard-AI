import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import subprocess
from datetime import datetime
import time

class NameDialog:
    def __init__(self):
        self.name = None
        self.age = None
        self.dialog = tk.Tk()
        self.dialog.title("Welcome!")
        self.dialog.geometry("400x300")
        self.dialog.configure(bg='#1e1e1e')
        
        # Center the dialog
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        self.dialog.geometry(f"400x300+{x}+{y}")
        
        # Welcome message
        welcome_label = tk.Label(
            self.dialog,
            text="👋 Welcome to Richard AI!",
            font=('Helvetica', 16, 'bold'),
            fg='#7289da',
            bg='#1e1e1e'
        )
        welcome_label.pack(pady=(20, 10))
        
        # Name frame
        name_frame = tk.Frame(self.dialog, bg='#1e1e1e')
        name_frame.pack(pady=10)
        
        # Name prompt
        name_label = tk.Label(
            name_frame,
            text="What's your name?",
            font=('Helvetica', 12),
            fg='#ffffff',
            bg='#1e1e1e'
        )
        name_label.pack()
        
        # Name entry
        self.name_entry = tk.Entry(
            name_frame,
            font=('Helvetica', 12),
            width=30,
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT,
            justify='center'
        )
        self.name_entry.pack(pady=5)
        
        # Age frame
        age_frame = tk.Frame(self.dialog, bg='#1e1e1e')
        age_frame.pack(pady=10)
        
        # Age prompt
        age_label = tk.Label(
            age_frame,
            text="How old are you?",
            font=('Helvetica', 12),
            fg='#ffffff',
            bg='#1e1e1e'
        )
        age_label.pack()
        
        # Age entry
        self.age_entry = tk.Entry(
            age_frame,
            font=('Helvetica', 12),
            width=10,
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT,
            justify='center'
        )
        self.age_entry.pack(pady=5)
        
        # Age requirement note
        age_note = tk.Label(
            self.dialog,
            text="(Must be 7 or older)",
            font=('Helvetica', 10),
            fg='#a0a0a0',
            bg='#1e1e1e'
        )
        age_note.pack()
        
        # Submit button
        submit_button = tk.Button(
            self.dialog,
            text="Let's Chat!",
            command=self.submit_info,
            font=('Helvetica', 12, 'bold'),
            bg='#7289da',
            fg='#ffffff',
            relief=tk.FLAT,
            padx=20,
            pady=5,
            activebackground='#677bc4'
        )
        submit_button.pack(pady=20)
        
        # Bind Enter key
        self.name_entry.bind('<Return>', lambda e: self.age_entry.focus())
        self.age_entry.bind('<Return>', lambda e: self.submit_info())
        
        # Set initial focus
        self.name_entry.focus()
    
    def submit_info(self):
        name = self.name_entry.get().strip()
        age_str = self.age_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter your name!")
            self.name_entry.focus()
            return
        
        if not age_str.isdigit():
            messagebox.showerror("Error", "Please enter a valid age!")
            self.age_entry.focus()
            return
        
        age = int(age_str)
        if age < 7:
            messagebox.showerror("Age Restriction", "Sorry, you must be 7 or older to use Richard AI!")
            self.age_entry.focus()
            return
        
        self.name = name
        self.age = age
        self.dialog.destroy()
    
    def get_info(self):
        self.dialog.mainloop()
        return self.name, self.age

class RichardBot:
    def __init__(self, user_name, user_age):
        self.user_name = user_name
        self.user_age = user_age
        self.root = tk.Tk()
        self.root.title("Richard - Your AI Comedy Companion")
        self.root.geometry("800x900")
        self.root.configure(bg='#1e1e1e')
        
        # Configure colors
        self.colors = {
            'bg': '#1e1e1e',
            'secondary_bg': '#2d2d2d',
            'accent': '#7289da',
            'text': '#ffffff',
            'text_secondary': '#a0a0a0',
            'success': '#43b581',
            'button_hover': '#677bc4'
        }
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Custom.TFrame", background=self.colors['bg'])
        self.style.configure("Secondary.TFrame", background=self.colors['secondary_bg'])
        self.style.configure("Custom.TButton", 
                           padding=10, 
                           font=('Helvetica', 12, 'bold'),
                           background=self.colors['accent'])
        
        # Voice settings
        self.voice = "Daniel"
        
        # Load jokes
        self.jokes = self.get_jokes()
        
        self.setup_gui()
        
    def setup_gui(self):
        # Main container
        main_frame = ttk.Frame(self.root, style="Custom.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header frame
        header_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Left side of header (Title)
        title_frame = ttk.Frame(header_frame, style="Custom.TFrame")
        title_frame.pack(side=tk.LEFT)
        
        # Title with emoji
        title_label = tk.Label(
            title_frame,
            text="🎭 Richard AI",
            font=('Helvetica', 32, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg']
        )
        title_label.pack(anchor='w')
        
        # Right side of header (Status and Time)
        info_frame = ttk.Frame(header_frame, style="Custom.TFrame")
        info_frame.pack(side=tk.RIGHT)
        
        # Time and Date display
        self.time_label = tk.Label(
            info_frame,
            text="",
            font=('Helvetica', 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        )
        self.time_label.pack(anchor='e', pady=(0, 5))
        
        # Status indicator
        self.status_label = tk.Label(
            info_frame,
            text="● Online",
            font=('Helvetica', 12),
            fg=self.colors['success'],
            bg=self.colors['bg']
        )
        self.status_label.pack(anchor='e')
        
        # Chat display with custom styling
        chat_frame = ttk.Frame(main_frame, style="Secondary.TFrame")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Helvetica', 12),
            bg=self.colors['secondary_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.chat_display.config(state=tk.DISABLED)
        
        # Input area
        input_frame = ttk.Frame(main_frame, style="Secondary.TFrame")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Message input with modern styling
        self.message_input = tk.Entry(
            input_frame,
            font=('Helvetica', 12),
            bg=self.colors['secondary_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief=tk.FLAT,
            bd=10
        )
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        self.message_input.bind('<Return>', lambda e: self.send_message())
        
        # Send button with hover effect
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            activebackground=self.colors['button_hover']
        )
        self.send_button.pack(side=tk.RIGHT, padx=10)
        
        # Joke button with custom styling
        self.joke_button = tk.Button(
            main_frame,
            text="🎯 Tell me a joke!",
            command=self.tell_joke,
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['success'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            activebackground='#3ca374'
        )
        self.joke_button.pack(pady=10)
        
        # Footer
        footer_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        footer_text = tk.Label(
            footer_frame,
            text="© 2024 Richard AI • Powered by AI",
            font=('Helvetica', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        )
        footer_text.pack(side=tk.RIGHT)
        
        # Welcome message
        self.add_message("Richard", f"👋 Hello {self.user_name}! I'm Richard, your AI comedy companion! I see you're {self.user_age} years old - perfect age for some good jokes! Type 'joke' or click the button below! 😊")
        
        # Start updating the time
        self.update_time()
    
    def get_jokes(self):
        return [
            {"setup": "Why don't programmers like nature?", "punchline": "It has too many bugs!"},
            {"setup": "What do you call a bear with no teeth?", "punchline": "A gummy bear!"},
            {"setup": "Why did the scarecrow win an award?", "punchline": "Because he was outstanding in his field!"},
            {"setup": "What do you call a fake noodle?", "punchline": "An impasta!"},
            {"setup": "Why did the math book look so sad?", "punchline": "Because it had too many problems!"},
            {"setup": "What do you call a can opener that doesn't work?", "punchline": "A can't opener!"},
            {"setup": "Why don't eggs tell jokes?", "punchline": "They'd crack up!"},
            {"setup": "What do you call a pig that does karate?", "punchline": "A pork chop!"},
            {"setup": "What do you call a sleeping bull?", "punchline": "A bulldozer!"},
            {"setup": "Why did the cookie go to the doctor?", "punchline": "Because it was feeling crumbly!"}
            # More jokes can be added here
        ]
    
    def speak(self, text):
        # Remove emojis and special characters before speaking
        cleaned_text = ''
        for char in text:
            # Only keep standard ASCII characters and basic punctuation
            if ord(char) < 128:
                cleaned_text += char
        # Use macOS say command to speak the cleaned text
        subprocess.Popen(['say', '-v', self.voice, cleaned_text])
    
    def add_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == "Richard":
            sender_color = self.colors['accent']
        else:
            sender_color = self.colors['success']
            
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"{sender}: ", "sender")
        self.chat_display.insert(tk.END, f"{message}\n\n", "message")
        
        # Configure tags
        self.chat_display.tag_config("timestamp", foreground=self.colors['text_secondary'])
        self.chat_display.tag_config("sender", foreground=sender_color, font=('Helvetica', 12, 'bold'))
        self.chat_display.tag_config("message", foreground=self.colors['text'])
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        # Speak the message if it's from Richard
        if sender == "Richard":
            self.speak(message)
    
    def tell_joke(self):
        joke = random.choice(self.jokes)
        self.add_message("Richard", joke["setup"])
        # Add delay for timing
        def tell_punchline():
            punchline = f"🎭 {joke['punchline']} 😄"
            self.add_message("Richard", punchline)
        # Longer delay for better timing with speech
        self.root.after(3000, tell_punchline)
    
    def send_message(self):
        message = self.message_input.get().strip()
        if message:
            self.add_message(self.user_name, message)
            self.message_input.delete(0, tk.END)
            
            if "joke" in message.lower():
                self.tell_joke()
            else:
                responses = [
                    "Want to hear a joke? Just ask!",
                    "I've got lots of jokes! Want to hear one?",
                    "I love telling jokes! Just type 'joke' or use the button!",
                    "Need a laugh? I'm here to help! Ask for a joke!"
                ]
                self.add_message("Richard", random.choice(responses))
    
    def update_time(self):
        # Update time every second
        current_time = datetime.now()
        date_str = current_time.strftime("%A, %B %d, %Y")
        time_str = current_time.strftime("%I:%M:%S %p")
        self.time_label.config(text=f"{date_str}\n{time_str}")
        self.root.after(1000, self.update_time)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Get user's info first
    name_dialog = NameDialog()
    user_name, user_age = name_dialog.get_info()
    
    if user_name and user_age:
        # Create and run the chatbot with the user's info
        bot = RichardBot(user_name, user_age)
        bot.run()
