# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Python CLI application that acts as a command-line interface to Google's Gemini AI model. The application takes a user prompt as a command line argument and returns the AI-generated response.

## Architecture

The codebase consists of a single main module (`main.py`) that:
- Uses `python-dotenv` to load environment variables from `.env`
- Authenticates with Google Gemini API using the `GEMINI_API_KEY` environment variable
- Accepts user prompts as command line arguments
- Makes API calls to `gemini-2.0-flash-001` model
- Outputs the response text and optionally usage metadata

## Development Setup

The project uses Python 3.13 and `uv` for package management.

### Environment Setup
1. Ensure you have a `.env` file with `GEMINI_API_KEY=your_api_key_here`
2. The virtual environment is located in `.venv/`

### Running the Application
```bash
python main.py "Your prompt here"
python main.py "Your prompt here" --verbose  # Shows token usage
```

### Package Management
This project uses `uv` for dependency management:
- `pyproject.toml` defines project metadata and dependencies
- `uv.lock` contains locked dependency versions
- Dependencies: `google-genai==1.12.1`, `python-dotenv==1.1.0`

## Key Files
- `main.py`: Single-file application containing all functionality
- `pyproject.toml`: Project configuration and dependencies
- `.env`: Contains the required `GEMINI_API_KEY`
- `.python-version`: Specifies Python 3.13

## Testing
No test framework is currently configured. The application can be tested by running it with various prompts.