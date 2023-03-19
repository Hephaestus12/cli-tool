import os


def list_files_and_folders(root_dir, level=0):
    for entry in os.listdir(root_dir):
        path = os.path.join(root_dir, entry)

        if os.path.isdir(path):
            print('  ' * level + f"[{entry}]")
            list_files_and_folders(path, level + 1)
        else:
            print('  ' * level + entry)


root_directory = "../wepromise/backend-service/code/src/main/kotlin"
list_files_and_folders(root_directory)
