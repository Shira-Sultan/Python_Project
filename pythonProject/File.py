import os
import shutil

def create_folder(path, name):
    if not os.path.exists(os.path.join(path, name)):
        os.mkdir(os.path.join(path, name))

def search_file(path, name):
    return os.path.exists(os.path.join(path, name))

def delete_folder(path, name_folder):
  shutil.rmtree(os.path.join(path, name_folder))

def delete_file(path, name_file):
    os.remove(os.path.join(path, name_file))

def empty_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Loop through each item in the directory
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Remove directory or file
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove directory and its contents
            else:
                os.remove(file_path)  # Remove file
    else:
        print(f"The directory {folder_path} does not exist.")


def clear_and_copy(path_current_commit, path_project):
    # מחיקת הקבצים והתקיות מה - working-copy
    for item in os.listdir(path_project):
        item_path = os.path.join(path_project, item)
        if item == ".wit":
            continue
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    # העתקת ה - commit הנבחר ל - working-copy
    for item in os.listdir(path_current_commit):
        src_path = os.path.join(path_current_commit, item)
        dest_path = os.path.join(path_project, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
