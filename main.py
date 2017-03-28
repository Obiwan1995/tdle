# -*- coding: utf-8 -*-
# !/usr/bin/python3

import os


def call_script_with_file(script_path, filename):
    if os.name == "nt":
        # Windows mode
        os.system("python " + script_path + " < data/" + filename)

    else:
        # Other
        os.system("cat data/" + filename + " | python3 " + script_path)


def main():
    print("Hello word")

    call_script_with_file("other/map_wordcount.py", "test.txt")


if __name__ == '__main__':
    main()
