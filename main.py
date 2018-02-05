#!/usr/bin/env python
__author__ = "liuhui"
import sys
import os


# try to import menu.py from lib
def main():
    try:
        lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "lib")
        sys.path.insert(0, lib_dir)
    except IOError:
        print("can not find the directory-lib, please check the path!\n"
              "you should make the main.py file and the lib directory\n"
              "in the same directory!")
        exit(1)
    import menu
    menu.main()


if __name__ == "__main__":
    main()
