import os
import sys
from google.genai import types

def get_files_info(working_directory, directory="."):


    base_path = os.path.realpath(working_directory)

    user_path = os.path.realpath(os.path.join(base_path, directory))

    if not user_path.startswith(base_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(user_path):
        return f'Error: "{directory}" is not a directory'

    dir_contents = []

    for item in os.listdir(user_path):
        file_size = os.path.getsize(os.path.join(user_path, item))
        is_dir = os.path.isdir(os.path.join(user_path, item))

        dir_contents.append(f'-{item}: file_size={file_size} bytes, is_dir={is_dir}')

    return "\n".join(dir_contents)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python get_files_info.py <working_directory> <directory>")
        sys.exit(1)

    working_dir_arg = sys.argv[1]
    directory_arg = sys.argv[2]

    result = get_files_info(working_dir_arg, directory_arg)
    print(result)
