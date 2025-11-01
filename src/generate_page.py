import os
import pathlib
from markdown_blocks import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating from {from_path} to {dest_path} using {template_path}")
    if os.path.exists(from_path):
        if os.path.exists(template_path):
            try:
                with open(from_path, 'r') as f:
                    from_path_content = f.read()

                with open(template_path, 'r') as f:
                    template_content = f.read()
            except Exception as e:
                return f"Something went wrong during the reading of the files: {e}"
        else:
            raise Exception(f"Path {template_path} does not exist.")
    else:
        raise Exception(f"Path {from_path} does not exist.")
    title = extract_title(from_path_content)
    html_string = markdown_to_html_node(from_path_content).to_html()
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_string)
    project_abs = os.path.abspath(".")
    dest_path_abs = os.path.abspath(dest_path)
    if not os.path.exists(dest_path):
        if not dest_path_abs.startswith(project_abs):
            raise Exception("Path of the src directory must be inside the project directory")
        try:
            os.makedirs(os.path.dirname(dest_path_abs), exist_ok=True)
        except Exception as e:
            return f"Error: creating src directory: {e}"
        if os.path.isdir(dest_path_abs):
            raise Exception("The src must be a file to write content")
        try:
            with open(dest_path_abs, 'w') as f:
                f.write(template_content)
        except Exception as e:
            return f"Error: something went wrong writing the file: {e}"
    else:
        if os.path.isdir(dest_path_abs):
            raise Exception("The src must be a file to write content")
        try:
            with open(dest_path_abs, 'w') as f:
                f.write(template_content)
        except Exception as e:
            return f"Error: something went wrong writing the file: {e}"
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_paths = get_paths(dir_path_content, [])
    for path in content_paths:
        relative_path = path.relative_to(dir_path_content)
        dest_path = os.path.join(dest_dir_path, relative_path.parent)
        os.makedirs(dest_path, exist_ok=True)
        generate_page(str(path), template_path, os.path.join(dest_path, f"{path.stem}.html"))

def get_paths(dir_path, path_list):
    content_paths = os.listdir(dir_path)
    for path in content_paths:
        join_path = os.path.join(dir_path, path)
        if os.path.isdir(join_path):
            get_paths(join_path, path_list)
        else:
            if join_path.endswith("md"):
                path_list.append(pathlib.Path(join_path))
    return path_list           
    
    
