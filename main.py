# -*- coding: utf-8 -*-
# !/usr/bin/python3

import os

def callScriptWithFile(scriptPath,fileName):
    if (os.name == "nt"):
        # Windows mode
        os.system("python "+scriptPath+" < data/"+fileName)

    else:
        # Other
        os.system("cat data/"+fileName+" | python3 "+scriptPath)

def main():
    print("Hello word")

    callScriptWithFile("other/map_wordcount.py","test.txt")




if __name__ == '__main__':
    main()
