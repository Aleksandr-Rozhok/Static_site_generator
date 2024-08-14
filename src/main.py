import os
import shutil

from utils import extract_title, markdown_to_html_node


def main():
    public_file_path = "./public"
    static_file_path = "./static"
    template_path = "./template.html"
    content_index_path = "./content"

    delete_old_public_files(public_file_path)
    copy_static_struct(static_file_path, public_file_path)
    generate_pages_recursive(content_index_path, template_path, public_file_path)
        
def delete_old_public_files(path):
    print("Start deleting process...")

    for filename in os.listdir(path):
        new_file_path = os.path.join(path, filename)

        if os.path.isfile(new_file_path) or os.path.islink(new_file_path):
            os.unlink(new_file_path)  
            print(f"Deleting {filename}...")
        elif os.path.isdir(new_file_path):
            print(f"Go into {filename}")
            delete_old_public_files(new_file_path)
            shutil.rmtree(new_file_path)
            print(f"Deleting {filename}...")

def copy_static_struct(from_path, to_path):
    for filename in os.listdir(from_path):
        new_from_file_path = os.path.join(from_path, filename)
        new_to_file_path = os.path.join(to_path, filename)
        
        if os.path.isfile(new_from_file_path) or os.path.islink(new_from_file_path):
            print(f"Copying {filename} from {new_from_file_path} into {new_to_file_path}...")
            shutil.copy(new_from_file_path, new_to_file_path, follow_symlinks=True)

        elif os.path.isdir(new_from_file_path):
            print(f"Go into {filename}")
            os.mkdir(new_to_file_path)
            print(f"Create new directory {filename}")
            copy_static_struct(new_from_file_path, new_to_file_path)

def generate_page(from_path, dest_path, template_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    content_file = open(from_path)
    template_file = open(template_path)

    content = content_file.read()
    content_of_template_file = template_file.read()

    html_string = markdown_to_html_node(content).to_html()
    title = extract_title(html_string)
    html_output = content_of_template_file.replace('{{ Title }}', title).replace('{{ Content }}', html_string)

    with open(dest_path + "/index.html", 'w') as file:
        file.write(html_output)
  
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_file = os.listdir(dir_path_content)

    for file in content_file:
        if os.path.isfile(os.path.join(dir_path_content, file)):
            generate_page(os.path.join(dir_path_content, file), dest_dir_path, template_path)
        else:
            os.mkdir(os.path.join(dest_dir_path, file))
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))


main()