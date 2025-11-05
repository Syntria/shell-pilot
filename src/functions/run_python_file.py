import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):

    base_path = os.path.realpath(working_directory)
    user_path = os.path.realpath(os.path.join(base_path, file_path))

    if not user_path.startswith(base_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(user_path):
        return f'Error: File "{file_path}" not found.'

    if not user_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        command = ["python", file_path] + args

        completed_process = subprocess.run(
            command,
            cwd=base_path,          # Run the command from the specified working directory
            capture_output=True,    # Capture stdout and stderr
            text=True,              # Decode output as text (strings)
            timeout=30              # Set a 30-second timeout
        )

        output_parts = []
        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()

        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}")
        
        if stderr:
            output_parts.append(f"STDERR:\n{stderr}")

        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")

        if not output_parts:
            return "No output produced."
        
        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds."
    except Exception as e:
        return f"Error: An exception occurred while executing the Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python script within the sandboxed environment and captures its output (stdout, stderr). Can pass command-line arguments to the script.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python (.py) file to execute (e.g., 'src/main.py')."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional. A list of string arguments to pass to the script. Each argument should be a separate string in the list.",
                items=types.Schema(type=types.Type.STRING)
            )
        },
        # The file_path is required, but args is optional.
        required=["file_path"]
    ),
)
