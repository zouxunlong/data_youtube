import os

for parent_dir, dirs, files in os.walk("./youtube8m"):
    for file in files:
        if os.path.getsize(os.path.join(parent_dir, file)) ==0:
            os.remove(os.path.join(parent_dir, file))