# -*- coding: utf-8 -*-
# !/usr/bin/python3

import os


def call_map_with_file(script_path, filename):
    if os.name == "nt":
        # Windows mode
        os.system("python " + script_path + " < data/" + filename)

    else:
        # Other
        os.system("cat data/" + filename + " | python3 " + script_path)


def call_mapreduce_with_file(script_path_map,script_path_reduce, filename):
    if os.name == "nt":
        # Windows mode
        os.system("python "+script_path_map+ " < data/" + filename+ " |  python " + script_path_reduce )

    else:
        # Other
        os.system("cat data/" + filename + " | python3 " + script_path_map + " | python3 "+script_path_reduce)

def main():
    print("Hello word")

    call_mapreduce_with_file("other/map_wordcount.py","other/reduce_wordcount.py", "test.txt")


if __name__ == '__main__':
    main()
