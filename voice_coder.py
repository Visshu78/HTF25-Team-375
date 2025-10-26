import speech_recognition as sr
import pyttsx3
import time

class BasicVoiceCoder:
    def __init__(self):
        print("🚀 Initializing Voice Coder...")
        
        # Speech recognition setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Text-to-speech setup
        self.tts_engine = pyttsx3.init()
        
        # Calibrate microphone
        print("🔊 Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("✅ Voice Coder Ready!")
    
    def speak(self, text):
        """Text-to-speech function"""
        print(f"🔊: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def generate_code(self, command):
        """Code generation logic"""
        command = command.lower()
        
        if "function" in command and "add" in command:
            return "def add(a, b):\n    return a + b"
        elif "loop" in command and "print" in command:
            return "for i in range(5):\n    print(i)"
        elif "hello" in command:
            return 'print("Hello, World!")'
        elif "list" in command:
            return "numbers = [1, 2, 3, 4, 5]"
        elif "if" in command and "else" in command:
            return "x = 10\nif x > 5:\n    print('Big')\nelse:\n    print('Small')"
        else:
            return f"# Command not understood: {command}"
    
    def listen_and_process(self):
        """Listen to voice and process command"""
        try:
            print("\n🎤 Listening... (Say your code command)")
            print("   You can say: 'create function', 'make loop', 'hello world'")
            
            with self.microphone as source:
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=6)
            
            # Convert speech to text
            command = self.recognizer.recognize_google(audio)
            print(f"✅ You said: '{command}'")
            
            return command
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected within 8 seconds")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand the audio")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def run(self):
        """Main program loop"""
        self.speak("Voice coder ready. Speak your code commands.")
        
        while True:
            try:
                # Listen for command
                command = self.listen_and_process()
                
                if command is None:
                    continue
                
                # Check for exit command
                if "exit" in command.lower() or "quit" in command.lower():
                    self.speak("Goodbye!")
                    break
                
                # Generate code
                code = self.generate_code(command)
                
                # Display code
                print("\n💻 GENERATED CODE:")
                print("=" * 40)
                print(code)
                print("=" * 40)
                
                # Save to file
                with open("generated_code.py", "w", encoding="utf-8") as f:
                    f.write(code)
                
                print("💾 Code saved to 'generated_code.py'")
                
                # Voice feedback
                self.speak("Code generated successfully")
                
                # Wait a bit before next command
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n👋 Program stopped by user")
                break

if __name__ == "__main__":
    print("🎯 VOICE ENABLED CODE ASSISTANT")
    print("=" * 50)
    
    coder = BasicVoiceCoder()
    coder.run()