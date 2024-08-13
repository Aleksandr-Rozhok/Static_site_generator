import os
import shutil


def main():
    public_file_path = "./public"
    static_file_path = "./static"

    delete_old_public_files(public_file_path)
    copy_static_struct(static_file_path, public_file_path)
        
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
        print(new_from_file_path)
        
        if os.path.isfile(new_from_file_path) or os.path.islink(new_from_file_path):
            print(f"Copying {filename} from {new_from_file_path} into {new_to_file_path}...")
            shutil.copy(new_from_file_path, new_to_file_path, follow_symlinks=True)

        elif os.path.isdir(new_from_file_path):
            print(f"Go into {filename}")
            os.mkdir(new_to_file_path)
            print(f"Create new directory {filename}")
            copy_static_struct(new_from_file_path, new_to_file_path)

main()