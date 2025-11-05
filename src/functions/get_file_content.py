import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):


    base_path = os.path.realpath(working_directory)

    user_path = os.path.realpath(os.path.join(base_path, file_path))

    if not user_path.startswith(base_path):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(user_path):
        return f'Error: "{file_path}" is not a file'


    with open(user_path, "r") as f:

        chunk = f.read(MAX_CHARS + 1)

        if len(chunk) > MAX_CHARS:
            has_more = True
            file_content_string = chunk[:MAX_CHARS]
        else:
            has_more = False
            file_content_string = chunk

    if has_more:
        truncated_message = f'[...File "{file_path}" truncated at 10000 characters]'
        file_content_string += truncated_message


    return file_content_string



schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a specified file. The content may be truncated if it is too long.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the file to be read (e.g., 'src/main.py' or 'README.md')."
            )
        },
        # The file_path is a required parameter for this function
        required=["file_path"]
    ),
)
