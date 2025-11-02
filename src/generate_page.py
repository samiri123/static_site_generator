import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node, extract_title

def generate_page(basepath, from_path, template_path, dest_path):
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
    template_content = template_content.replace('/href="', basepath)
    template_content = template_content.replace('/src="', basepath)
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
    


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(basepath, from_path, template_path, dest_path)
        else:
            generate_pages_recursive(basepath, from_path, template_path, dest_path)
         
    
    
