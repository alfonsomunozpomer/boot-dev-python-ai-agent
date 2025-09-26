import os
from textwrap import dedent
from google.genai import types

def write_file(working_directory, file_path, content):
    destination_file_path = os.path.join(working_directory, file_path)

    working_directory_absolute_path = os.path.abspath(working_directory)
    destination_file_absolute_path = os.path.abspath(destination_file_path)
    if (
        not os.path.commonpath([working_directory_absolute_path, destination_file_absolute_path]) ==
          working_directory_absolute_path
    ):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.makedirs(os.path.dirname(destination_file_absolute_path), exist_ok=True)
        with open(destination_file_absolute_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'
    
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=dedent("""\
                    Writes the specified content to a file, constrained to the working directory. 
                    Creates any necessary directories along the path."""),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file."
            ),
        },
    ),
)