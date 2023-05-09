import os

extension = ".py"

folder_path = "./seeds/"
files = os.listdir(folder_path)

py_files = [file for file in files if file.endswith(extension)]
py_files.sort()

for file in py_files:
    print("(process)", file)
    file_path = os.path.join(folder_path, file)
    os.system("python {}".format(file_path))