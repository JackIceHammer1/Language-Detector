from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.util import ClassNotFound
from langdetect import detect, LangDetectException
from difflib import get_close_matches

# Example database of known languages and code snippets
language_database = {
    "python": ["print('Hello, world!')", "def func(): pass", "import os"],
    "sql": ["SELECT * FROM users;", "INSERT INTO table_name (column1, column2) VALUES (value1, value2);"],
    "html": ["<html><body>Hello, world!</body></html>", "<div class='container'>"],
    "java": ["public class HelloWorld { public static void main(String[] args) { System.out.println('Hello, World!'); } }"],
    "english": ["Hello, how are you?", "This is a test sentence."],
    "spanish": ["Hola, ¿cómo estás?", "Esta es una frase de prueba."],
    "french": ["Bonjour, comment ça va?", "Ceci est une phrase de test."]
}

def detect_language(code):
    try:
        lexer = guess_lexer(code)
        language = lexer.name
    except ClassNotFound:
        language = "Unknown"
    return language

def detect_human_language(text):
    try:
        language = detect(text)
    except LangDetectException:
        language = "Unknown"
    return language

def cross_check_with_database(input_text):
    all_texts = sum(language_database.values(), [])
    matches = get_close_matches(input_text, all_texts, n=1, cutoff=0.5)
    if matches:
        for lang, snippets in language_database.items():
            if matches[0] in snippets:
                return lang
    return "Unknown"

if __name__ == "__main__":
    user_input = input("Enter the text or code snippet: ")
    
    prog_language = detect_language(user_input)
    human_language = detect_human_language(user_input)
    db_language = cross_check_with_database(user_input)
    
    if prog_language != "Unknown":
        print(f"The detected programming language is: {prog_language}")
    elif human_language != "Unknown":
        print(f"The detected human communication language is: {human_language}")
    elif db_language != "Unknown":
        print(f"The language cross-referenced from the database is: {db_language}")
    else:
        print("The language could not be detected.")
