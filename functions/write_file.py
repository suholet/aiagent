import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes the content to the file at the specified path relative to the working directory. If the file has some content, replaces it. If the file doesn't exist, creates it.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="File path to write content to the file, relative to the working directory",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="Content to write to the file",
                ),
            },
        ),
    )

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    # os.makedirs(target_file_path, exist_ok=True)
    if not os.path.exists(working_dir_abs):
        os.makedirs(working_dir_abs)

    try:
        with open(target_file_path, "w") as f:
            # Overwrite the file content
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except:
        raise Exception("Error: something went wrong while writing to the file")