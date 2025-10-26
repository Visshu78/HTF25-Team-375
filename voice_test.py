import speech_recognition as sr

def test_microphone():
    r = sr.Recognizer()
    
    print("🎤 Testing microphone... Bol kuch bhi!")
    print("3 seconds...")
    
    try:
        with sr.Microphone() as source:
            # Background noise adjust karo
            print("🔊 Adjusting for background noise...")
            r.adjust_for_ambient_noise(source, duration=2)
            
            print("🎤 Bol ab...")
            audio = r.listen(source, timeout=10)
        
        # Speech to text conversion
        text = r.recognize_google(audio)
        print(f"✅ Tumne kaha: '{text}'")
        return text
        
    except sr.UnknownValueError:
        print("❌ Audio samajh nahi aaya")
        return None
    except sr.WaitTimeoutError:
        print("❌ Kuch boli nahi")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    test_microphone()