# AI Agent CLI

An intelligent coding agent powered by Google's Gemini AI model with function calling capabilities.

## Features

- **AI Coding Agent**: Intelligent assistant that can understand and execute coding tasks
- **Function Calling**: The agent can perform file operations through integrated functions:
  - List files and directories
  - Read file contents
  - Write or overwrite files
  - Execute Python files with optional arguments
- **Iterative Problem Solving**: Runs up to 20 iterations to complete complex tasks
- **Verbose Mode**: Display detailed function calls and token usage statistics
- **Environment-based Configuration**: Secure API key management through .env files

## Prerequisites

- Python 3.13+
- Google Gemini API key

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-agent
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Or if using `uv`:
   ```bash
   uv sync
   ```

3. Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

### Basic Coding Tasks
Ask the agent to perform coding tasks - it will automatically use the available functions:
```bash
python main.py "Create a simple calculator in Python"
python main.py "Show me the contents of main.py"
python main.py "List all Python files in the current directory"
```

### Verbose Mode
Display detailed function calls and token usage statistics:
```bash
python main.py "Fix any bugs in calculator.py" --verbose
```

## Example

```bash
$ python main.py "Create a hello world program"
Calling function: write_file
-> File written successfully
I've created a simple "Hello, World!" program in hello_world.py

$ python main.py "Run the hello world program" --verbose
User prompt: Run the hello world program
Calling function: run_python_file({'file_path': 'hello_world.py'})
-> Hello, World!

I've successfully run the hello_world.py program. The output was "Hello, World!"
Prompt tokens: 12
Response tokens: 45
```

## Configuration

The application requires a Google Gemini API key. You can obtain one from the [Google AI Studio](https://makersuite.google.com/app/apikey).

Set your API key in the `.env` file:
```
GEMINI_API_KEY=your_actual_api_key_here
```

## Architecture

The agent operates within a working directory (`./calculator`) and can perform the following operations:

- **get_files_info**: List files and directories
- **get_file_content**: Read the contents of any file
- **write_file**: Create or overwrite files
- **run_python_file**: Execute Python scripts with optional arguments

The agent uses an iterative approach, making up to 20 function calls to complete complex tasks.

## Dependencies

- `google-genai`: Official Google Generative AI Python client
- `python-dotenv`: Load environment variables from .env files

## Error Handling

- If no prompt is provided, the application will display an error message
- If the API key is missing or invalid, the Google client will raise an authentication error
- Function call errors are handled gracefully and reported back to the agent
- The agent will attempt to complete tasks within the maximum iteration limit (20 loops)
- Network issues will be propagated as exceptions from the underlying HTTP client