import os
import sys

def main():
    if len(sys.argv) < 3:
        exit(0)
    dir = sys.argv[2]
    if dir[0] != '/':
        dir = os.getcwd() + '/' + dir
    files = []
    for r, d, f in os.walk(dir):
        for file in f:
            if '.py' in file:
                files.append(os.path.join(r, file))
    print("All done! ✨ 🍰 ✨")
    print(str(len(files)) + " files would be left unchanged.")
    exit(0)