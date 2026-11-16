import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        print(abs_working_dir)
        print(abs_file_path)
        return f'Error: "{file_path}" is not in the working dir'
    
    parent_dir = os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f"Could not create parent dirs: {parent_dir} = {e}"     

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} character'
    except Exception as e:
        return f"Failed to write to {file_path} exception ,e :{e}"



schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes content to a file inside the allowed working directory. "
        "Creates parent directories if they do not exist."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path relative to the allowed working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file."
            ),
        },
        required=["file_path", "content"]
    ),
)