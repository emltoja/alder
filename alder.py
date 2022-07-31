#! /usr/bin/env python

# Directory tree generator

from os import path as os_path, getcwd
from colored import fg
from treedata import DirectoryTree

if __name__ == '__main__':
    fg(231)
    print(DirectoryTree(os_path.basename(getcwd())).get_tree())
