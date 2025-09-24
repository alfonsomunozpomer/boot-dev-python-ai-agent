# AI Agent CLI

A simple command-line interface for interacting with Google's Gemini AI model.

## Features

- Send prompts directly from the command line
- Get AI-generated responses using Gemini 2.0 Flash
- Optional verbose mode to display token usage statistics
- Environment-based API key configuration

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

### Basic Usage
```bash
python main.py "What is the capital of France?"
```

### Verbose Mode
Display token usage statistics along with the response:
```bash
python main.py "Explain quantum computing" --verbose
```

## Example

```bash
$ python main.py "Write a haiku about coding"
Code flows like water,
Logic branching through the night,
Bugs become features.

$ python main.py "What is machine learning?" --verbose
Machine learning is a subset of artificial intelligence that focuses on...

User prompt: What is machine learning?
Prompt tokens: 6
Response tokens: 142
```

## Configuration

The application requires a Google Gemini API key. You can obtain one from the [Google AI Studio](https://makersuite.google.com/app/apikey).

Set your API key in the `.env` file:
```
GEMINI_API_KEY=your_actual_api_key_here
```

## Dependencies

- `google-genai`: Official Google Generative AI Python client
- `python-dotenv`: Load environment variables from .env files

## Error Handling

- If no prompt is provided, the application will display an error message
- If the API key is missing or invalid, the Google client will raise an authentication error
- Network issues will be propagated as exceptions from the underlying HTTP client