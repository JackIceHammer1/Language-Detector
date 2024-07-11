from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.util import ClassNotFound
from langdetect import detect, LangDetectException

def detect_language(code):
    try:
        # Guess the lexer for the provided code
        lexer = guess_lexer(code)
        language = lexer.name
    except ClassNotFound:
        language = "Unknown"

    return language

def detect_human_language(text):
    try:
        # Detect the human language
        language = detect(text)
    except LangDetectException:
        language = "Unknown"

    return language

if __name__ == "__main__":
    # Read input from the user
    user_input = input("Enter the text or code snippet: ")
    
    # Detect programming language
    prog_language = detect_language(user_input)
    
    # Detect human communication language
    human_language = detect_human_language(user_input)
    
    # Determine and print the type of language detected
    if prog_language != "Unknown":
        print(f"The detected programming language is: {prog_language}")
    elif human_language != "Unknown":
        print(f"The detected human communication language is: {human_language}")
    else:
        print("The language could not be detected.")
