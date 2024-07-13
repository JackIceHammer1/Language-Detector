from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.util import ClassNotFound
from langdetect import detect, LangDetectException
from difflib import get_close_matches

# Expanded database of known languages and code snippets
language_database = {
    "python": [
        "print('Hello, world!')", "def func(): pass", "import os",
        "for i in range(10): print(i)", "class MyClass:", "self.attribute = value"
    ],
    "sql": [
        "SELECT * FROM users;", "INSERT INTO table_name (column1, column2) VALUES (value1, value2);",
        "UPDATE table_name SET column1 = value1 WHERE condition;", "DELETE FROM table_name WHERE condition;"
    ],
    "html": [
        "<html><body>Hello, world!</body></html>", "<div class='container'>",
        "<a href='http://example.com'>Link</a>", "<h1>Title</h1>", "<p>Paragraph</p>"
    ],
    "java": [
        "public class HelloWorld { public static void main(String[] args) { System.out.println('Hello, World!'); } }",
        "public static void main(String[] args)", "System.out.println('Output');", "int x = 5;", "String s = 'text';"
    ],
    "javascript": [
        "console.log('Hello, world!');", "function myFunction() { return; }", "var x = 10;", "let y = 'text';", 
        "const z = true;", "document.getElementById('id').value;"
    ],
    "c": [
        "#include <stdio.h>", "int main() { printf('Hello, world!'); return 0; }", "int x = 5;", "char c = 'A';",
        "printf('Output');", "scanf('%d', &x);"
    ],
    "cpp": [
        "#include <iostream>", "int main() { std::cout << 'Hello, world!'; return 0; }", "int x = 5;", 
        "std::string s = 'text';", "std::cout << 'Output';"
    ],
    "csharp": [
        "using System;", "class Program { static void Main() { Console.WriteLine('Hello, world!'); } }", 
        "int x = 5;", "string s = 'text';", "Console.WriteLine('Output');"
    ],
    "ruby": [
        "puts 'Hello, world!'", "def my_method; end", "@variable = value", "class MyClass", "if condition; end"
    ],
    "php": [
        "<?php echo 'Hello, world!'; ?>", "$variable = 'value';", "function myFunction() { return; }", 
        "if ($condition) { }", "$_POST['key'];"
    ],
    "go": [
        "package main", "import 'fmt'", "func main() { fmt.Println('Hello, world!') }", "var x int = 5", 
        "s := 'text'", "fmt.Println('Output')"
    ],
    "swift": [
        "print('Hello, world!')", "func myFunction() {}", "var x = 5", "let s = 'text'", "class MyClass {}"
    ],
    "kotlin": [
        "fun main() { println('Hello, world!') }", "val x = 5", "var s = 'text'", "class MyClass", 
        "if (condition) { }"
    ],
    "r": [
        "print('Hello, world!')", "x <- 5", "y <- 'text'", "myFunction <- function() {}", "if (condition) { }"
    ],
    "matlab": [
        "disp('Hello, world!')", "x = 5;", "y = 'text';", "function myFunction()", "if condition; end"
    ],
    "perl": [
        "print 'Hello, world!';", "my $variable = 'value';", "sub myFunction { return; }", "if ($condition) { }"
    ],
    "bash": [
        "echo 'Hello, world!'", "variable=value", "if [ condition ]; then fi", "for i in {1..10}; do done"
    ],
    "typescript": [
        "console.log('Hello, world!');", "function myFunction(): void { return; }", "let x: number = 10;", 
        "const y: string = 'text';", "interface MyInterface { }"
    ],
    "english": [
        "Hello, how are you?", "This is a test sentence.", "Good morning.", "How is the weather today?", 
        "Can you help me with this?"
    ],
    "spanish": [
        "Hola, ¿cómo estás?", "Esta es una frase de prueba.", "Buenos días.", "¿Cómo está el clima hoy?", 
        "¿Puedes ayudarme con esto?"
    ],
    "french": [
        "Bonjour, comment ça va?", "Ceci est une phrase de test.", "Bon matin.", "Quel temps fait-il aujourd'hui?", 
        "Pouvez-vous m'aider avec ça?"
    ],
    "german": [
        "Hallo, wie geht's?", "Dies ist ein Testsatz.", "Guten Morgen.", "Wie ist das Wetter heute?", 
        "Kannst du mir damit helfen?"
    ],
    "chinese": [
        "你好，你怎么样？", "这是一个测试句子。", "早上好。", "今天的天气怎么样？", "你能帮我这个吗？"
    ],
    "japanese": [
        "こんにちは、お元気ですか？", "これはテスト文です。", "おはようございます。", "今日の天気はどうですか？", 
        "これを手伝ってくれませんか？"
    ]
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
