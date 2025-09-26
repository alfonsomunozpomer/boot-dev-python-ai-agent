import os
import sys
from google.genai import types

def get_files_info(working_directory, directory="."):
    absolute_path = os.path.abspath(os.path.join(working_directory, directory))

    if (
        os.path.commonpath([os.path.abspath(working_directory), absolute_path]) !=
        os.path.abspath(working_directory)
    ):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'
    
    try:        
        return '\n'.join(
            map(
                lambda dir_entry: _format_path_info(os.path.join(absolute_path, dir_entry)),
                os.listdir(absolute_path)
            )
        )
    except Exception as e:
        return f'Error: {str(e)}'
        
def _format_path_info(file_path):
    return f'- {os.path.basename(file_path)}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}'


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                default=".",
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


if __name__ == "__main__":
    # get_files_info('/home/alf/devsorted/boot.dev/ai-agent', '../..')
    # print(get_files_info('calculator', '../..'))
    print(get_files_info(sys.argv[1], sys.argv[2]))
