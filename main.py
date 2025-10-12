import argparse
import os
from dotenv import load_dotenv
from google.genai import Client
from google.genai.types import GenerateContentConfig, Content, FunctionCall, Part
from textwrap import dedent
from call_function import available_functions, call_function
from config import MAX_AGENT_LOOP_COUNT


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Coding Agent")
    parser.add_argument("prompt", type=str, help="The prompt for the AI agent")
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()
    if not args.prompt:
        print("Error: Please provide a prompt as a command line argument.")
        exit(1)
    verbose = args.verbose

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = Client(api_key=api_key)

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

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        Content(role="user", parts=[Part(text=user_prompt)]),
    ]

    for _ in range(MAX_AGENT_LOOP_COUNT):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            messages.extend(
                map(lambda candidate: candidate.content, response.candidates)
            )

            if not response.function_calls:
                print(response.text)
                if verbose:
                    print_token_usage(response)
                exit(0)

            user_messages = handle_function_calls(response.function_calls, verbose)
            messages.extend(user_messages)

            if verbose:
                print_token_usage(response)

        except Exception as e:
            print(f"Error: {e}")
            break


def handle_function_calls(
    response_function_calls: list[FunctionCall], verbose: bool
) -> list[Content]:
    user_messages = []

    for function_call_part in response_function_calls:
        function_call_result = call_function(function_call_part, verbose=verbose)

        if not (
            function_call_result.parts
            and function_call_result.parts[0].function_response
        ):
            raise Exception("Function did not return a response")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        user_messages.append(Content(role="user", parts=function_call_result.parts))

    return user_messages


def print_token_usage(response) -> None:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
