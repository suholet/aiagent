import os
from google.genai import types
from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Reads the first MAX_CHARS characters from the file at the specified path relative to the working directory, providing the comment if the file is larger and was trunkated",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="File path to read content from the file, relative to the working directory",
                ),
            },
        ),
    )

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

    print(working_dir_abs)
    print(target_file_path)

    # Will be True or False
    valid_target_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

    if not valid_target_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file_path, "r") as f:
            # Read the first MAX_CHARS from the file
            content = f.read(MAX_CHARS)

            # After reading the first MAX_CHARS check if there are more and add a message.
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content
    except:
        raise Exception("Error: something went wrong while reading the file")