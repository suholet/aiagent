import os, subprocess

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if target_file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file_path]

    try:
        if args != None:
            command.extend(args)

        prcs = subprocess.run(command, text=True, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ""

        if prcs.returncode != 0:
            output += f"Process exited with code {prcs.returncode}\n"
        
        if prcs.stdout == "" or prcs.stderr == "":
            output += f"No output produced\n"
        else:
            output += f"STDOUT: {prcs.stdout}\nSTDERR: {prcs.stderr}\n"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"