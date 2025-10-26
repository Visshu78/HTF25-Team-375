def generate_code(command):
    """
    Simple rule-based code generator
    """
    command = command.lower()
    
    # Pre-defined commands
    if "function" in command and "add" in command:
        return """def add(a, b):
    return a + b"""
    
    elif "loop" in command and "print" in command:
        return """for i in range(5):
    print(f"Number: {i}")"""
    
    elif "hello" in command or "hello world" in command:
        return 'print("Hello, World!")'
    
    elif "list" in command and "number" in command:
        return """numbers = [1, 2, 3, 4, 5]
for num in numbers:
    print(num)"""
    
    elif "if" in command and "else" in command:
        return """age = 18
if age >= 18:
    print("Adult")
else:
    print("Minor")"""
    
    else:
        return f"# Could not understand command: {command}\n# Try: 'create function', 'make loop', 'hello world'"

# Test function
def test_generator():
    test_commands = [
        "create function add numbers",
        "make loop print numbers", 
        "hello world",
        "create list of numbers",
        "if else statement"
    ]
    
    print("🧪 Testing Code Generator...")
    for cmd in test_commands:
        code = generate_code(cmd)
        print(f"\nCommand: '{cmd}'")
        print("Generated Code:")
        print(code)
        print("-" * 40)

if __name__ == "__main__":
    test_generator()