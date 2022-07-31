#! /usr/bin/env python

# Directory tree generator

import argparse 

from os import path as os_path, getcwd
from colored import fg
from treedata import DirectoryTree

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='alder',
        description='Create tree of current directory'
    )

    parser.add_argument('--maxdepth', type=int, default=5, 
                         help='depth of a tree (default: 5)')
    parser.add_argument('--maxlen', type=int, default=20,
                         help='length of a tree (default: 20)')

    args = parser.parse_args()

    fg(231)
    print(DirectoryTree(
        os_path.basename(getcwd()),
        max_depth=args.maxdepth,
        max_len=args.maxlen).get_tree())
