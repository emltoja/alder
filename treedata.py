'''

Module containing classes that are backbones of tree generating

'''

from pathlib import Path
from os import getcwd, listdir
from colored import fg

class Data:

    '''

    Class abstracting both directories as files in tree structure

    Parameters
    ----------
    name
        name of current data (not equivalent to the path e.g dev vs. C:\\dev)
    parent
        parent directory (default None for root)

    '''

    def __init__(self, name: str, path: str = None, parent = None):

        self.name = name
        self.parent = parent
        self.path = Path(path) if path else self.get_path()
        self.level = parent.level + 1 if parent else -1
        self.prefix = ' ' * ((len(self.name) - 1) // 2)

        if parent:    
            if name == listdir(parent.get_abs_path())[-1]:
                self.prefix = self.parent.prefix + '   ' + ' ' * ((len(self.name) - 1) // 2)
            else: 
                self.prefix = self.parent.prefix + '|  ' + ' ' * ((len(self.name) - 1) // 2)


    def get_path(self) -> Path:

        ''' Get path of current data relative to path of parent '''

        return Path(str(self.parent.path) + '\\' + self.name)

    def get_abs_path(self) -> Path:

        ''' Get absolute path of data '''

        return self.path.absolute()


class DirectoryTree(Data):

    '''

    Class representing directories in tree stucture.
    Inherits from Data class

    '''

    def __init__(self, name: str, path: str = None, parent: Data = None, max_depth = 5, max_len = 20):

        super().__init__(name, path, parent)
        self.max_depth = max_depth
        self.max_len = max_len
        self.content = self.get_content()


    def __str__(self) -> str:

        ''' String representation for debug purposes'''

        return f'({self.name}; {list(map(str, self.content))})'


    def get_content(self) -> list[Data]:

        '''

        Get content of directory as list of instances
        of either DirectoryTree or File classes

        '''

        content = []

        for child in listdir(self.path):

            child_path = Path(str(self.path) + '\\' + child)

            if child_path.is_dir():
                content.append(DirectoryTree(
                    child,
                    parent=self,
                    max_depth=self.max_depth,
                    max_len=self.max_len))
            else:
                content.append(File(child, self))

        return content


    def get_tree(self) -> str:

        '''

        Get string respresentation of tree with blue color
        for files and green for directories

        '''


        result = self.parent.prefix + f'|--{fg(2)}{self.name}{fg(231)}' + '\n' \
            if self.parent \
                else fg(98) + self.name  + fg(231) + '\n'

        if self.content:

            for child in self.content[:min(len(self.content), self.max_len)]:

                if child.level >= self.max_depth:
                    result += (self.prefix + '.\n') * 3
                    break

                result += child.get_tree()

            if len(self.content) > self.max_len:
                result += (self.prefix + '.\n') * 3

        return result


class File(Data):

    '''

    Class representing files in tree stucture.

    Parameters
    ----------
    name
        name of a file (same case as in dirs)
    parent
        as above

    '''

    def __init__(self, name: str, parent: DirectoryTree):

        super().__init__(name, parent=parent)

    def __str__(self) -> str:

        return self.name

    def get_tree(self) -> str:

        ''' String repr of file with prefixes and colouring in tree '''

        return self.parent.prefix + f'|--{fg(4)}{self.name}{fg(231)}' + '\n' \
            if self.parent \
                else f'|--{fg(4)}{self.name}{fg(231)}' + '\n'
