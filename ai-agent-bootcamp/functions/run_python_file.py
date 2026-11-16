import os
import subprocess
import sys
from google.genai import types


def run_python_file(working_directory: str, file_path: str, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working dir'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        output = subprocess.run(
            [sys.executable, file_path, *args],
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text=True
        )

        final_string = f"""
STDOUT:
{output.stdout}
STDERR:
{output.stderr}
"""

        if output.stdout == "" and output.stderr == "":
            final_string = "No output produced.\n"

        if output.returncode != 0:
            final_string += f"Process exited with code {output.returncode}"

        return final_string

    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file inside the allowed working directory "
        "and returns its stdout and stderr output."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file path relative to the allowed working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional command-line arguments to pass to the Python file."
            ),
        },
        required=["file_path"]
    ),
)