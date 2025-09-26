import os
import subprocess
from textwrap import dedent
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    destination_file_path = os.path.join(working_directory, file_path)

    working_directory_absolute_path = os.path.abspath(working_directory)
    destination_file_absolute_path = os.path.abspath(destination_file_path)
    if (
        not os.path.commonpath([working_directory_absolute_path, destination_file_absolute_path]) ==
          working_directory_absolute_path
    ):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(destination_file_absolute_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ['python', destination_file_absolute_path, *args],
            timeout=30,
            capture_output=True,
            cwd=working_directory_absolute_path
        )

        log = []
        if (completed_process.stdout):
            log.append(f"STDOUT: {completed_process.stdout.decode('utf-8')}")
        if (completed_process.stderr):
            log.append(f"STDERR: {completed_process.stderr.decode('utf-8')}")
        if (completed_process.returncode != 0):
            log.append(f"Process exited with code {completed_process.returncode}")

        return '\n'.join(log) if log else "No output produced."
        
    except Exception as e:
        return f'Error: {str(e)}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=dedent("""\
                    Executes the specified Python file with optional arguments, constrained to the working directory. 
                    Captures and returns the standard output and error produced during execution."""),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python script.",
            ),
        },
    ),
)
