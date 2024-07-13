from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
from langdetect import detect, detect_langs, LangDetectException, DetectorFactory
from difflib import get_close_matches
import logging

# Set the seed for langdetect to ensure deterministic results
DetectorFactory.seed = 0

# Database of code snippets and common phrases for various languages
language_database = {
    "python": [
        "def fetch_data(url):", "import requests", "for i in range(1, 11):", "if __name__ == '__main__':",
        "with open('file.txt') as f:", "try: except Exception as e:", "print(", "def main():"
    ],
    "sql": [
        "SELECT id, name FROM users WHERE active = 1;", "INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?);",
        "UPDATE users SET last_login = NOW() WHERE id = ?;", "DELETE FROM sessions WHERE last_activity < NOW() - INTERVAL '30 days';"
    ],
    "html": [
        "<div class='container'>", "<form action='/submit' method='post'>", "<input type='text' name='username'>",
        "<button type='submit'>Submit</button>", "<link rel='stylesheet' href='styles.css'>", "<header>"
    ],
    "java": [
        "public class User {", "private String name;", "public static void main(String[] args) {",
        "System.out.println('Welcome');", "List<String> names = new ArrayList<>();", "public static"
    ],
    "javascript": [
        "function fetchData(url) {", "document.getElementById('submit').addEventListener('click', function() {",
        "const data = await fetch('/api/data');", "if (response.ok) {", "let items = [1, 2, 3];"
    ],
    "c": [
        "#include <stdio.h>", "int main(int argc, char *argv[]) {", "printf('Processing data...');",
        "FILE *file = fopen('data.txt', 'r');", "if (file == NULL) {"
    ],
    "cpp": [
        "#include <iostream>", "int main() {", "std::vector<int> numbers;", "std::cout << 'Enter number: ';",
        "std::string name;"
    ],
    "csharp": [
        "using System;", "class Program {", "static void Main(string[] args) {", "Console.WriteLine('Starting application');",
        "List<int> values = new List<int>();"
    ],
    "ruby": [
        "class User", "def initialize(name)", "users.each do |user|", "File.open('file.txt', 'r') do |file|",
        "puts 'Processing data...'"
    ],
    "php": [
        "<?php", "$result = mysqli_query($conn, 'SELECT * FROM users');", "if ($result) {", "function fetchData($url) {",
        "echo 'Data processed';"
    ],
    "go": [
        "package main", "import 'fmt'", "func main() {", "if err != nil {", "response, err := http.Get(url)"
    ],
    "swift": [
        "import UIKit", "class ViewController: UIViewController {", "let url = URL(string: 'https://example.com')",
        "if let data = try? Data(contentsOf: url) {", "print('Data fetched successfully')"
    ],
    "kotlin": [
        "fun main() {", "val names = listOf('Alice', 'Bob')", "if (response.isSuccessful) {", "class User(val name: String)",
        "println('Data processing...')"
    ],
    "r": [
        "data <- read.csv('data.csv')", "plot(data$column)", "for (i in 1:10) {", "if (is.na(value)) {",
        "print('Data analysis complete')"
    ],
    "matlab": [
        "data = readtable('data.csv');", "plot(data.Column1);", "for i = 1:10", "if isempty(value)",
        "disp('Data processing complete')"
    ],
    "perl": [
        "use strict;", "my $dbh = DBI->connect($dsn, $user, $password);", "if ($dbh) {", "sub process_data {",
        "print 'Data processing complete';"
    ],
    "bash": [
        "echo 'Starting process'", "for i in {1..10}; do", "if [ -f 'file.txt' ]; then", "while read -r line; do",
        "curl -X POST -d 'data=value' http://example.com/api"
    ],
    "typescript": [
        "const fetchData = async (url: string) => {", "interface User {", "let response: Response;",
        "if (response.ok) {", "console.log('Data fetched successfully');"
    ],
    "english": [
        "hi", "hello", "and", "what", "who", "good", "that",
        "Could you please send me the report by EOD?", "Let's schedule a meeting for next Monday.",
        "I need help with the new project.", "The weather is quite nice today.", "Do you have any suggestions?"
    ],
    "spanish": [
        "hola", "buenos días", "y", "qué", "quién", "bueno", "eso",
        "¿Podrías enviarme el informe antes del final del día?", "Vamos a programar una reunión para el próximo lunes.",
        "Necesito ayuda con el nuevo proyecto.", "El clima está muy agradable hoy.", "¿Tienes alguna sugerencia?"
    ],
    "french": [
        "salut", "bonjour", "et", "quoi", "qui", "bon", "ça",
        "Pourriez-vous m'envoyer le rapport d'ici la fin de la journée ?", "Programmons une réunion pour lundi prochain.",
        "J'ai besoin d'aide pour le nouveau projet.", "Le temps est très agréable aujourd'hui.", "Avez-vous des suggestions?"
    ],
    "german": [
        "hallo", "guten Morgen", "und", "was", "wer", "gut", "das",
        "Könnten Sie mir bitte den Bericht bis zum Ende des Tages schicken?", "Lassen Sie uns ein Treffen für nächsten Montag planen.",
        "Ich brauche Hilfe mit dem neuen Projekt.", "Das Wetter ist heute sehr schön.", "Haben Sie irgendwelche Vorschläge?"
    ],
    "chinese": [
        "你好", "早上好", "和", "什么", "谁", "好", "那",
        "请你在今天结束前发给我报告吗？", "我们安排下周一开会。", "我需要帮助新项目。", "今天天气很好。", "你有任何建议吗？"
    ],
    "japanese": [
        "こんにちは", "おはようございます", "と", "何", "誰", "良い", "それ",
        "今日中にレポートを送ってください。", "来週の月曜日に会議をスケジュールしましょう。", "新しいプロジェクトの助けが必要です。",
        "今日はとてもいい天気ですね。", "何か提案がありますか？"
    ]
}

def identify_language_with_confidence(text):
    """
    Identify the language of the given text using Pygments for code and langdetect for natural language.
    Returns the identified language and the confidence score.
    """
    try:
        # Try to identify the language using Pygments (code detection)
        lexer = guess_lexer(text)
        language = lexer.name.lower()
        if language in language_database:
            confidence = 1.0  # Pygments doesn't provide confidence scores
            logging.info(f"Pygments identified language: {language} with confidence {confidence}")
            return language, confidence
        else:
            logging.warning(f"Pygments identified language '{language}' not found in database, falling back to natural language detection.")
    except ClassNotFound:
        logging.warning("Pygments failed to identify language, falling back to natural language detection.")

    # If Pygments fails or the language is not in the database, use langdetect
    try:
        detected_languages = detect_langs(text)
        language = detected_languages[0].lang
        confidence = detected_languages[0].prob
        logging.info(f"langdetect identified language: {language} with confidence {confidence}")
    except LangDetectException:
        logging.error("Language could not be identified.")
        return None, None
    
    # Map natural language codes to full names if necessary
    language_map = {
        'en': 'english',
        'es': 'spanish',
        'fr': 'french',
        'de': 'german',
        'zh-cn': 'chinese',
        'ja': 'japanese'
    }
    
    return language_map.get(language, language), confidence

def get_code_snippets(language):
    """
    Retrieve a list of code snippets for the given language from the database.
    """
    language = language.lower()
    if language in language_database:
        logging.info(f"Retrieved code snippets for language: {language}")
        return language_database[language]
    else:
        logging.warning(f"Language '{language}' not found in database.")
        return []

def find_closest_language(language):
    """
    Find the closest matching language in the database for the given language.
    """
    language = language.lower()
    all_languages = language_database.keys()
    closest_match = get_close_matches(language, all_languages, n=1)
    if closest_match:
        logging.info(f"Closest match found: {closest_match[0]} for language: {language}")
        return closest_match[0]
    else:
        logging.warning(f"No close match found for language: {language}")
        return None

def check_common_errors(code_snippet):
    """
    Check for common errors in the given code snippet and return suggestions.
    """
    errors = []
    if 'print ' in code_snippet and not code_snippet.startswith("print("):
        errors.append("Did you mean print(...)?")
    if 'import ' in code_snippet and 'import(' in code_snippet:
        errors.append("Did you mean 'import ...' instead of 'import(...)'?")
    return errors

# User feedback mechanism
def get_user_feedback(detected_language, confidence):
    """
    Get feedback from the user about the accuracy of the detected language.
    """
    print(f"Detected language: {detected_language} with confidence {confidence:.2f}")
    feedback = input("Is this correct? (yes/no): ").strip().lower()
    return feedback == 'yes'

def show_help():
    """
    Display help and documentation on how to use the script.
    """
    print("Language and Code Snippet Identifier")
    print("Usage:")
    print("  - Enter your text or code snippet when prompted.")
    print("  - The script will identify the language and provide relevant code snippets.")
    print("  - If the language detection is not accurate, it will suggest the closest match for confirmation.")
    print("  - In case of any error, the script will provide guidance on what to do next.")
    print("Languages supported:")
    print("  - Programming languages: Python, SQL, HTML, Java, JavaScript, C, C++, C#, Ruby, PHP, Go, Swift, Kotlin, R, MATLAB, Perl, Bash, TypeScript")
    print("  - Natural languages: English, Spanish, French, German, Chinese, Japanese")
    print("Examples of usage:")
    print("  - Entering 'def my_function():' will detect Python and provide related snippets.")
    print("  - Entering 'SELECT * FROM users;' will detect SQL and provide related snippets.")
    print("  - Entering 'Hello, how are you?' will detect English and provide common phrases.")

def main():
    """
    Main function to identify language, provide code snippets, handle user input for confirmation, show help,
    and handle errors with suggestions.
    """
    logging.basicConfig(level=logging.INFO)
    
    while True:
        user_input = input("Enter your text (or 'help' for instructions, 'exit' to quit): ").strip()
        
        if user_input.lower() == 'help':
            show_help()
            continue
        elif user_input.lower() == 'exit':
            break
        
        detected_language, confidence = identify_language_with_confidence(user_input)
        
        if detected_language:
            print(f"Detected language: {detected_language} with confidence {confidence:.2f}")
            snippets = get_code_snippets(detected_language)
            
            if snippets:
                print(f"Code snippets for {detected_language}:")
                for snippet in snippets:
                    print(f"- {snippet}")
                    errors = check_common_errors(snippet)
                    if errors:
                        for error in errors:
                            print(f"Error: {error}")
            else:
                print(f"No snippets found for {detected_language}.")
                closest_language = find_closest_language(detected_language)
                if closest_language:
                    confirmation = input(f"Did you mean: {closest_language}? (yes/no): ")
                    if confirmation.lower() == 'yes':
                        snippets = get_code_snippets(closest_language)
                        if snippets:
                            print(f"Code snippets for {closest_language}:")
                            for snippet in snippets:
                                print(f"- {snippet}")
                                errors = check_common_errors(snippet)
                                if errors:
                                    for error in errors:
                                        print(f"Error: {error}")
                    else:
                        print("No matching language found.")
        else:
            print("Could not detect the language of the text. Please try entering a different text or check the input for any errors.")

if __name__ == "__main__":
    main()
