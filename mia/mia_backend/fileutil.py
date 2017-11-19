import os
import re

def get_files_by_ext(src, dst, ext, end_ext):
    """ gets a list of files from a directory by extension 'ext'.
        Returns a list of tuples in the format
        (src/filename.ext, dst/filename.end_ext)
        If end_ext is none, filename is kept the same
     """
    good_files = []
    ext_re = ext

    if not ext_re.startswith('.'):
        ext_re = '.' + ext_re

    directory_files = [f for f in os.walk(src)]
    for directory_tuple in directory_files:
        for file in directory_tuple[2]:
            if file.endswith(ext_re):
                # if the file has the extension, add to good_file list which is a tuple of
                # (current directory, destination directory)
                if end_ext:
                    f_renamed = file.replace(ext, end_ext)
                else:
                    f_renamed = file

                good_files.append((os.path.join(directory_tuple[0], file),
                                   os.path.join(dst, f_renamed)))

    return good_files
