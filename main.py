import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from textwrap import dedent
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="AI Coding Agent")
    parser.add_argument("prompt", type=str, help="The prompt for the AI agent")
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()
    if not args.prompt:
        print("Error: Please provide a prompt as a command line argument.")
        exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = dedent(
        """\
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan.
        You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory.
        You do not need to specify the working directory in your function calls
        as it is automatically injected for security reasons."""
    )
    user_prompt = args.prompt

    if args.verbose:
        print(f'User prompt: {user_prompt}')

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose=args.verbose)

        if not (
            function_call_result.parts and 
            function_call_result.parts[0].function_response and
            function_call_result.parts[0].function_response.response
        ):
            raise Exception("Function did not return a response")

        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    if args.verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')


if __name__ == "__main__":
    main()
