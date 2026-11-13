import os

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working dir'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'

    try:
        file_content_string = ""

        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)

            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS]
                file_content_string += (
                    f'\n[Truncated: file content exceeds {MAX_CHARS} characters]'
                )

        return file_content_string

    except Exception as e:
        return f'Error: Cannot read file: {e}'