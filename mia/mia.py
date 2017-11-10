import os
import shutil


def main():
    """ main loop for mia program """


if __name__ == "__main__":
    main()


basedir = os.path.abspath(os.path.dirname(__file__))

dest = os.environ.get('DEST_DIR')

src_files = os.listdir(basedir)
for file_name in src_files:
    full_file_name = os.path.join(basedir, file_name)
    if (os.path.isfile(full_file_name)):
        shutil.copy(full_file_name, dest)
