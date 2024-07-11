from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.util import ClassNotFound

def detect_language(code):
    try:
        # Guess the lexer for the provided code
        lexer = guess_lexer(code)
        language = lexer.name
    except ClassNotFound:
        language = "Unknown"

    return language

if __name__ == "__main__":
    # Read code input from the user
    code_snippet = input("Enter the code snippet: ")
    
    # Detect and print the language for the provided code snippet
    language = detect_language(code_snippet)
    print(f"The detected programming language is: {language}")
