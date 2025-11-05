import os
from google.genai import types

def write_file(working_directory, file_path, content):

    base_path = os.path.realpath(working_directory)

    user_path = os.path.realpath(os.path.join(base_path, file_path))

    if not user_path.startswith(base_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        with open(user_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to a specified file, overwriting the file if it already exists. Creates the file if it does not exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the file to be written to (e.g., 'src/main.py' or 'output.txt')."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file."
            ),
        },
        # Both parameters are required for the function to work
        required=["file_path", "content"]
    ),
)
