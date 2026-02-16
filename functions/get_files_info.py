import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                ),
            },
        ),
    )

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir_path = os.path.normpath(os.path.join(working_dir_abs, directory))

    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir_path]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir_path):
        return f'Error: "{directory}" is not a directory'
    
    dir_list =  os.listdir(target_dir_path)

    try:
        result_str = ""
        for item in dir_list:
            full_path = f"{target_dir_path}/{item}"
            name = item 
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            result_str += f"- {name}: file_size={file_size} bytes, is_dir={is_dir}\n"
        return result_str
    except:
        raise Exception("Error: something went wrong")