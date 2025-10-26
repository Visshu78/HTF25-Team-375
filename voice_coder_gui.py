import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import speech_recognition as sr
import pyttsx3
import subprocess
import os

class VoiceCoderGUI:
    def __init__(self):
        # Setup main window
        self.root = tk.Tk()
        self.root.title("🎤 Voice Code Assistant - HACKATHON")
        self.root.geometry("750x600")
        self.root.configure(bg="#f0f0f0")
        
        # Speech components
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        
        # Language selection
        self.language_var = tk.StringVar(value="python")
        
        # Calibrate microphone once
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except:
            print("⚠️  Microphone not available")
        
        self.create_widgets()
        self.update_status("✅ Ready! Click 'Start Voice' and speak")
    
    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="🎤 VOICE CODE ASSISTANT",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title.pack(pady=10)
        
        # Language Selection Frame
        lang_frame = tk.Frame(self.root, bg="#f0f0f0")
        lang_frame.pack(pady=5)
        
        tk.Label(lang_frame, text="Language:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(side=tk.LEFT)
        
        languages = [("Python", "python"), ("JavaScript", "javascript"), ("Java", "java")]
        for text, lang in languages:
            tk.Radiobutton(
                lang_frame, 
                text=text, 
                variable=self.language_var, 
                value=lang,
                bg="#f0f0f0",
                command=self.on_language_change
            ).pack(side=tk.LEFT, padx=5)
        
        # Big Voice Button
        self.voice_btn = tk.Button(
            self.root,
            text="🎤 START VOICE COMMAND",
            command=self.start_voice_command,
            bg="#27ae60",
            fg="white",
            font=("Arial", 16, "bold"),
            height=2,
            width=25,
            relief="raised",
            bd=3
        )
        self.voice_btn.pack(pady=15)
        
        # Status Label
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        self.status_label.pack(pady=5)
        
        # Code Display Area
        code_frame = tk.Frame(self.root, bg="#f0f0f0")
        code_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        tk.Label(code_frame, text="Generated Code:", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(anchor="w")
        
        self.code_display = scrolledtext.ScrolledText(
            code_frame,
            height=15,
            width=80,
            font=("Consolas", 11),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="white",
            selectbackground="#3d3d3d"
        )
        self.code_display.pack(fill="both", expand=True)
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        # Run Code Button
        tk.Button(
            button_frame,
            text="▶️ Run Code",
            command=self.execute_code,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            height=1
        ).pack(side=tk.LEFT, padx=5)
        
        # Save Button
        tk.Button(
            button_frame,
            text="💾 Save As",
            command=self.save_as_file,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            height=1
        ).pack(side=tk.LEFT, padx=5)
        
        # Clear Button
        tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_code,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            height=1
        ).pack(side=tk.LEFT, padx=5)
        
        # Help Text
        help_text = "Try: 'create function' • 'make loop' • 'hello world' • 'create list' • 'if else' • 'create class'"
        help_label = tk.Label(
            self.root,
            text=help_text,
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#7f8c8d"
        )
        help_label.pack(pady=10)
    
    def on_language_change(self):
        """When language is changed"""
        lang = self.language_var.get()
        self.update_status(f"Language changed to: {lang}", "blue")
        self.speak(f"Now generating {lang} code")
    
    def generate_code(self, command):
        """Enhanced code generator with multiple languages"""
        command = command.lower()
        lang = self.language_var.get()
        
        # Python Code
        if lang == "python":
            if "function" in command and "add" in command:
                return "def add(a, b):\n    return a + b"
            elif "loop" in command and "print" in command:
                return "for i in range(5):\n    print(f'Number: {i}')"
            elif "hello" in command:
                return 'print("Hello, World!")'
            elif "list" in command:
                return "numbers = [1, 2, 3, 4, 5]\nfor num in numbers:\n    print(num)"
            elif "if" in command and "else" in command:
                return "age = 18\nif age >= 18:\n    print('Adult')\nelse:\n    print('Minor')"
            elif "class" in command:
                return "class Person:\n    def __init__(self, name):\n        self.name = name\n    def greet(self):\n        print(f'Hello, {self.name}')"
        
        # JavaScript Code
        elif lang == "javascript":
            if "function" in command and "add" in command:
                return "function add(a, b) {\n    return a + b;\n}"
            elif "loop" in command and "print" in command:
                return "for (let i = 0; i < 5; i++) {\n    console.log(`Number: ${i}`);\n}"
            elif "hello" in command:
                return 'console.log("Hello, World!");'
            elif "list" in command:
                return "const numbers = [1, 2, 3, 4, 5];\nnumbers.forEach(num => console.log(num));"
            elif "if" in command and "else" in command:
                return "const age = 18;\nif (age >= 18) {\n    console.log('Adult');\n} else {\n    console.log('Minor');\n}"
            elif "class" in command:
                return "class Person {\n    constructor(name) {\n        this.name = name;\n    }\n    greet() {\n        console.log(`Hello, ${this.name}`);\n    }\n}"
        
        # Java Code
        elif lang == "java":
            if "function" in command and "add" in command:
                return "public static int add(int a, int b) {\n    return a + b;\n}"
            elif "loop" in command and "print" in command:
                return "for (int i = 0; i < 5; i++) {\n    System.out.println(\"Number: \" + i);\n}"
            elif "hello" in command:
                return 'System.out.println("Hello, World!");'
            elif "list" in command:
                return "int[] numbers = {1, 2, 3, 4, 5};\nfor (int num : numbers) {\n    System.out.println(num);\n}"
            elif "if" in command and "else" in command:
                return "int age = 18;\nif (age >= 18) {\n    System.out.println(\"Adult\");\n} else {\n    System.out.println(\"Minor\");\n}"
            elif "class" in command:
                return "class Person {\n    String name;\n    \n    public Person(String name) {\n        this.name = name;\n    }\n    \n    public void greet() {\n        System.out.println(\"Hello, \" + name);\n    }\n}"
        
        # Default fallback
        return f"# Command not understood: {command}\n# Language: {lang}\n\n# Try these commands:\n# - 'create function add numbers'\n# - 'make loop print numbers'\n# - 'hello world'\n# - 'create list of numbers'\n# - 'if else statement'\n# - 'create class person'"
    
    def speak(self, text):
        """Text-to-speech"""
        def tts_thread():
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        threading.Thread(target=tts_thread, daemon=True).start()
    
    def update_status(self, message, color="black"):
        """Update status label"""
        self.status_label.config(text=message, fg=color)
        self.root.update()
    
    def start_voice_command(self):
        """Start voice recognition in separate thread"""
        self.voice_btn.config(bg="#e74c3c", text="🎤 LISTENING... SPEAK NOW")
        self.update_status("🎤 Listening... Speak your code command", "red")
        
        # Start voice recognition in background thread
        threading.Thread(target=self.voice_recognition_thread, daemon=True).start()
    
    def voice_recognition_thread(self):
        """Voice recognition in background thread"""
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=6)
            
            command = self.recognizer.recognize_google(audio)
            
            # Process in main thread
            self.root.after(0, self.process_voice_command, command)
            
        except sr.WaitTimeoutError:
            self.root.after(0, self.update_status, "⏰ No speech detected", "orange")
        except sr.UnknownValueError:
            self.root.after(0, self.update_status, "❌ Could not understand audio", "red")
        except Exception as e:
            self.root.after(0, self.update_status, f"❌ Error: {str(e)}", "red")
        
        # Reset button
        self.root.after(0, lambda: self.voice_btn.config(bg="#27ae60", text="🎤 START VOICE COMMAND"))
    
    def process_voice_command(self, command):
        """Process the voice command and generate code"""
        self.update_status(f"🎯 Heard: '{command}'", "blue")
        
        # Generate code
        code = self.generate_code(command)
        
        # Update code display
        self.code_display.delete(1.0, tk.END)
        self.code_display.insert(1.0, code)
        
        # Save to file
        try:
            filename = f"generated_code.{self.get_file_extension()}"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)
            self.update_status(f"✅ Code generated & saved to '{filename}'", "green")
        except Exception as e:
            self.update_status(f"❌ Save failed: {str(e)}", "red")
        
        # Voice feedback
        self.speak("Code generated successfully")
    
    def get_file_extension(self):
        """Get file extension based on language"""
        extensions = {
            "python": "py",
            "javascript": "js", 
            "java": "java"
        }
        return extensions.get(self.language_var.get(), "txt")
    
    def execute_code(self):
        """Execute the generated code"""
        code = self.code_display.get(1.0, tk.END).strip()
        if not code or code.startswith("# Command not understood"):
            messagebox.showwarning("Warning", "No valid code to execute!")
            return
        
        lang = self.language_var.get()
        filename = f"temp_code.{self.get_file_extension()}"
        
        try:
            # Save code to temporary file
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)
            
            self.update_status("🔄 Executing code...", "orange")
            
            # Execute based on language
            if lang == "python":
                result = subprocess.run(["python", filename], capture_output=True, text=True, timeout=10)
            elif lang == "javascript":
                result = subprocess.run(["node", filename], capture_output=True, text=True, timeout=10)
            elif lang == "java":
                # Java requires compilation first
                compile_result = subprocess.run(["javac", filename], capture_output=True, text=True)
                if compile_result.returncode == 0:
                    classname = filename.replace(".java", "")
                    result = subprocess.run(["java", classname], capture_output=True, text=True, timeout=10)
                else:
                    result = compile_result
            
            # Show output
            output = result.stdout if result.stdout else result.stderr
            if output:
                messagebox.showinfo("Execution Result", f"Output:\n{output}")
                self.update_status("✅ Code executed successfully", "green")
            else:
                messagebox.showinfo("Execution Result", "Code executed (no output)")
                self.update_status("✅ Code executed (no output)", "green")
                
        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "Code execution timeout!")
            self.update_status("❌ Execution timeout", "red")
        except Exception as e:
            messagebox.showerror("Error", f"Execution failed: {str(e)}")
            self.update_status("❌ Execution failed", "red")
        finally:
            # Cleanup temporary files
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                if lang == "java" and os.path.exists("TempCode.class"):
                    os.remove("TempCode.class")
            except:
                pass
    
    def save_as_file(self):
        """Save code to a specific file"""
        code = self.code_display.get(1.0, tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "No code to save!")
            return
        
        # In real implementation, you'd use filedialog
        # For hackathon, we'll use simple naming
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = self.get_file_extension()
        filename = f"voice_code_{timestamp}.{extension}"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)
            self.update_status(f"💾 Saved as '{filename}'", "green")
            messagebox.showinfo("Success", f"Code saved as:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {str(e)}")
    
    def clear_code(self):
        """Clear the code display"""
        self.code_display.delete(1.0, tk.END)
        self.update_status("📝 Code display cleared", "blue")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🚀 Starting Enhanced Voice Coder GUI...")
    app = VoiceCoderGUI()
    app.run()