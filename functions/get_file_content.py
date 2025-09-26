import sys
import os
from textwrap import dedent
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    destination_file_path = os.path.join(working_directory, file_path)

    working_directory_absolute_path = os.path.abspath(working_directory)
    destination_file_absolute_path = os.path.abspath(destination_file_path)
    if (
        not os.path.commonpath([working_directory_absolute_path, destination_file_absolute_path]) ==
          working_directory_absolute_path
    ):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(destination_file_absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(destination_file_absolute_path, 'r') as f:
            file_content_string = f.read(MAX_CHARS)
            return file_content_string
    except Exception as e:
        return f'Error: {str(e)}'

    pass


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=dedent(f"""\
                    Shows the content of the specified file, constrained to the working directory. 
                    Truncates content to a maximum number of characters defined by the constant 
                    MAX_CHARS; currently  set to {MAX_CHARS}."""),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory."
            ),
        },
    ),
)