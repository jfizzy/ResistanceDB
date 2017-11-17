import os
import re

def get_files_by_ext(src, dst, ext, end_ext):
    """ gets a list of files from a directory by extension 'ext'. Returns a list 
        of tuples in the format (src/filename.ext, dst/filename.end_ext)

        If end_ext is none, filename is kept the same
     """
    files = []
    good_files = []
    ext_re = ext

    if not ext_re.startswith('*.'):
            if '.' in ext_re:
                re.sub(".", ".*.", ext_re)
            elif '*' in ext_re:
                re.sub('\*', ".*.", ext_re)
            else:
                ext_re = ".*." + ext_re

    directory_files = [f for f in os.walk(src)]
    for directory_tuple in directory_files:
        for f in directory_tuple[2]:
            if re.findall(ext_re, f):
                # if the file has the extension, add to good_file list which is a tuple of 
                # (current directory, destination directory)
                if end_ext:
                    f_renamed = f.replace(ext, end_ext)
                else:
                    f_renamed = f

                good_files.append((os.path.join(directory_tuple[0], f), os.path.join(dst, f_renamed)))

    return good_files
