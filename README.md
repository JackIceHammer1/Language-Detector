# Language and Code Snippet Identifier

This project identifies the language of a given text or code snippet using Pygments for code detection and langdetect for natural language detection. It provides relevant code snippets and handles user input for language confirmation and common error checking.

## Features

- **Language Detection**: Identifies programming languages and natural languages from the input text.
- **Code Snippets**: Provides relevant code snippets based on the detected language.
- **Common Error Checking**: Identifies common errors in the provided code snippets.
- **User Feedback**: Allows users to confirm or correct the detected language.
- **Help and Documentation**: Provides instructions and usage examples to guide users.

## Supported Languages

### Programming Languages
- Python
- SQL
- HTML
- Java
- JavaScript
- C
- C++
- C#
- Ruby
- PHP
- Go
- Swift
- Kotlin
- R
- MATLAB
- Perl
- Bash
- TypeScript

### Natural Languages
- English
- Spanish
- French
- German
- Chinese
- Japanese

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/language-snippet-identifier.git
    cd language-snippet-identifier
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the script:
    ```sh
    python main.py
    ```

2. Follow the prompts:
    - Enter your text or code snippet when prompted.
    - The script will identify the language and provide relevant code snippets.
    - If the language detection is not accurate, it will suggest the closest match for confirmation.
    - In case of any error, the script will provide guidance on what to do next.

## Examples

- Entering `def my_function():` will detect Python and provide related snippets.
- Entering `SELECT * FROM users;` will detect SQL and provide related snippets.
- Entering `Hello, how are you?` will detect English and provide common phrases.