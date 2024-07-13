from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.util import ClassNotFound
from langdetect import detect, LangDetectException
from difflib import get_close_matches
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Combined database of known languages and code snippets with more realistic examples
language_database = {
    "python": [
        "def fetch_data(url):", "import requests", "for i in range(1, 11):", "if __name__ == '__main__':",
        "with open('file.txt') as f:", "try: except Exception as e:", "print('Hello, world!')", "def func(): pass", "import os",
        "for i in range(10): print(i)", "class MyClass:", "self.attribute = value"
    ],
    "sql": [
        "SELECT id, name FROM users WHERE active = 1;", "INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?);",
        "UPDATE users SET last_login = NOW() WHERE id = ?;", "DELETE FROM sessions WHERE last_activity < NOW() - INTERVAL '30 days';",
        "SELECT * FROM users;", "INSERT INTO table_name (column1, column2) VALUES (value1, value2);",
        "UPDATE table_name SET column1 = value1 WHERE condition;", "DELETE FROM table_name WHERE condition;"
    ],
    "html": [
        "<div class='container'>", "<form action='/submit' method='post'>", "<input type='text' name='username'>",
        "<button type='submit'>Submit</button>", "<link rel='stylesheet' href='styles.css'>", "<html><body>Hello, world!</body></html>", "<div class='container'>",
        "<a href='http://example.com'>Link</a>", "<h1>Title</h1>", "<p>Paragraph</p>"
    ],
    "java": [
        "public class User {", "private String name;", "public static void main(String[] args) {",
        "System.out.println('Welcome');", "List<String> names = new ArrayList<>();", "public class HelloWorld { public static void main(String[] args) { System.out.println('Hello, World!'); } }",
        "public static void main(String[] args)", "System.out.println('Output');", "int x = 5;", "String s = 'text';"
    ],
    "javascript": [
        "function fetchData(url) {", "document.getElementById('submit').addEventListener('click', function() {",
        "const data = await fetch('/api/data');", "if (response.ok) {", "let items = [1, 2, 3];", "console.log('Hello, world!');", "function myFunction() { return; }", "var x = 10;", "let y = 'text';", 
        "const z = true;", "document.getElementById('id').value;"
    ],
    "c": [
        "#include <stdio.h>", "int main(int argc, char *argv[]) {", "printf('Processing data...');",
        "FILE *file = fopen('data.txt', 'r');", "if (file == NULL) {", "#include <stdio.h>", "int main() { printf('Hello, world!'); return 0; }", "int x = 5;", "char c = 'A';",
        "printf('Output');", "scanf('%d', &x);"
    ],
    "cpp": [
        "#include <iostream>", "int main() {", "std::vector<int> numbers;", "std::cout << 'Enter number: ';",
        "std::string name;", "#include <iostream>", "int main() { std::cout << 'Hello, world!'; return 0; }", "int x = 5;", 
        "std::string s = 'text';", "std::cout << 'Output';"
    ],
    "csharp": [
        "using System;", "class Program {", "static void Main(string[] args) {", "Console.WriteLine('Starting application');",
        "List<int> values = new List<int>();", "using System;", "class Program { static void Main() { Console.WriteLine('Hello, world!'); } }", 
        "int x = 5;", "string s = 'text';", "Console.WriteLine('Output');"
    ],
    "ruby": [
        "class User", "def initialize(name)", "users.each do |user|", "File.open('file.txt', 'r') do |file|",
        "puts 'Processing data...'", "puts 'Hello, world!'", "def my_method; end", "@variable = value", "class MyClass", "if condition; end"
    ],
    "php": [
        "<?php", "$result = mysqli_query($conn, 'SELECT * FROM users');", "if ($result) {", "function fetchData($url) {",
        "echo 'Data processed';", "<?php echo 'Hello, world!'; ?>", "$variable = 'value';", "function myFunction() { return; }", 
        "if ($condition) { }", "$_POST['key'];"
    ],
    "go": [
        "package main", "import 'fmt'", "func main() {", "if err != nil {", "response, err := http.Get(url)", "package main", "import 'fmt'", "func main() { fmt.Println('Hello, world!') }", "var x int = 5", 
        "s := 'text'", "fmt.Println('Output')"
    ],
    "swift": [
        "import UIKit", "class ViewController: UIViewController {", "let url = URL(string: 'https://example.com')",
        "if let data = try? Data(contentsOf: url) {", "print('Data fetched successfully')", "print('Hello, world!')", "func myFunction() {}", "var x = 5", "let s = 'text'", "class MyClass {}"
    ],
    "kotlin": [
        "fun main() {", "val names = listOf('Alice', 'Bob')", "if (response.isSuccessful) {", "class User(val name: String)",
        "println('Data processing...')", "fun main() { println('Hello, world!') }", "val x = 5", "var s = 'text'", "class MyClass", 
        "if (condition) { }"
    ],
    "r": [
        "data <- read.csv('data.csv')", "plot(data$column)", "for (i in 1:10) {", "if (is.na(value)) {",
        "print('Data analysis complete')", "print('Hello, world!')", "x <- 5", "y <- 'text'", "myFunction <- function() {}", "if (condition) { }"
    ],
    "matlab": [
        "data = readtable('data.csv');", "plot(data.Column1);", "for i = 1:10", "if isempty(value)",
        "disp('Data processing complete')", "disp('Hello, world!')", "x = 5;", "y = 'text';", "function myFunction()", "if condition; end"
    ],
    "perl": [
        "use strict;", "my $dbh = DBI->connect($dsn, $user, $password);", "if ($dbh) {", "sub process_data {",
        "print 'Data processing complete';", "print 'Hello, world!';", "my $variable = 'value';", "sub myFunction { return; }", "if ($condition) { }"
    ],
    "bash": [
        "echo 'Starting process'", "for i in {1..10}; do", "if [ -f 'file.txt' ]; then", "while read -r line; do",
        "curl -X POST -d 'data=value' http://example.com/api", "echo 'Hello, world!'", "variable=value", "if [ condition ]; then fi", "for i in {1..10}; do done"
    ],
    "typescript": [
        "const fetchData = async (url: string) => {", "interface User {", "let response: Response;",
        "if (response.ok) {", "console.log('Data fetched successfully');", "console.log('Hello, world!');", "function myFunction(): void { return; }", "let x: number = 10;", 
        "const y: string = 'text';", "interface MyInterface { }"
    ],
    "english": [
        "Could you please send me the report by EOD?", "Let's schedule a meeting for next Monday.",
        "I need help with the new project.", "The weather is quite nice today.", "Do you have any suggestions?", "Hello, how are you?", "This is a test sentence.", "Good morning.", "How is the weather today?", 
        "Can you help me with this?"
    ],
    "spanish": [
        "¿Podrías enviarme el informe antes del final del día?", "Vamos a programar una reunión para el próximo lunes.",
        "Necesito ayuda con el nuevo proyecto.", "El clima está muy agradable hoy.", "¿Tienes alguna sugerencia?", "Hola, ¿cómo estás?", "Esta es una frase de prueba.", "Buenos días.", "¿Cómo está el clima hoy?", 
        "¿Puedes ayudarme con esto?"
    ],
    "french": [
        "Pourriez-vous m'envoyer le rapport d'ici la fin de la journée?", "Programmons une réunion pour lundi prochain.",
        "J'ai besoin d'aide pour le nouveau projet.", "Le temps est très agréable aujourd'hui.", "Avez-vous des suggestions?", "Bonjour, comment ça va?", "Ceci est une phrase de test.", "Bon matin.", "Quel temps fait-il aujourd'hui?", 
        "Pouvez-vous m'aider avec ça?"
    ],
    "german": [
        "Könnten Sie mir bitte den Bericht bis zum Ende des Tages zusenden?", "Lassen Sie uns ein Meeting für nächsten Montag planen.",
        "Ich brauche Hilfe mit dem neuen Projekt.", "Das Wetter ist heute sehr schön.", "Haben Sie irgendwelche Vorschläge?", "Hallo, wie geht's?", "Dies ist ein Testsatz.", "Guten Morgen.", "Wie ist das Wetter heute?", 
        "Kannst du mir damit helfen?"
    ],
    "chinese": [
        "你能在今天结束前把报告发给我吗？", "让我们安排下周一的会议。", "我需要帮助处理新项目。", "今天天气很好。",
        "你有什么建议吗？", "你好，你怎么样？", "这是一个测试句子。", "早上好。", "今天的天气怎么样？", "你能帮我这个吗？"
    ],
    "japanese": [
        "今日中にレポートを送っていただけますか？", "来週の月曜日に会議を設定しましょう。", "新しいプロジェクトで助けが必要です。",
        "今日はとてもいい天気です。", "何か提案はありますか？", "こんにちは、お元気ですか？", "これはテスト文です。", "おはようございます。", "今日の天気はどうですか？", 
        "これを手伝ってくれませんか？"
    ]
}

def identify_language(text):
    """
    Identify the language of the given text using Pygments for code and langdetect for natural language.
    """
    try:
        # Try to identify the language using Pygments (code detection)
        lexer = guess_lexer(text)
        language = lexer.name.lower()
        logging.info(f"Pygments identified language: {language}")
    except ClassNotFound:
        # If Pygments fails, try using langdetect (natural language detection)
        try:
            language = detect(text)
            logging.info(f"langdetect identified language: {language}")
        except LangDetectException:
            logging.error("Language could not be identified.")
            return None
    
    # Map natural language codes to full names if necessary
    language_map = {
        'en': 'english',
        'es': 'spanish',
        'fr': 'french',
        'de': 'german',
        'zh-cn': 'chinese',
        'ja': 'japanese'
    }
    
    return language_map.get(language, language)

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
    Find the closest matching language in the database to handle typos or similar language names.
    """
    closest_matches = get_close_matches(language, language_database.keys())
    if closest_matches:
        closest_language = closest_matches[0]
        logging.info(f"Did you mean: {closest_language}?")
        return closest_language
    else:
        logging.warning(f"No close match found for language: {language}")
        return None

# Example usage
if __name__ == "__main__":
    sample_text = "import requests\nresponse = requests.get('https://example.com')"
    detected_language = identify_language(sample_text)
    
    if detected_language:
        snippets = get_code_snippets(detected_language)
        if not snippets:
            # Try finding the closest language match if no snippets found
            closest_language = find_closest_language(detected_language)
            if closest_language:
                snippets = get_code_snippets(closest_language)
        
        if snippets:
            for snippet in snippets:
                print(snippet)
        else:
            logging.error("No code snippets available.")
    else:
        logging.error("Failed to detect language.")
