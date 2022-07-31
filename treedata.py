from pathlib import Path
from os import getcwd, listdir
from colored import fg

class Data:

    def __init__(self, name: str, parent = None):

        self.name = name
        self.parent = parent
        self.path = self.get_path()
        self.prefix = self.parent.prefix + '|  ' + ' ' * ((len(self.name) - 1) // 2) \
            if parent \
                else ' ' * ((len(self.name) - 1) // 2)


    def get_path(self):

        return Path(str(self.parent.get_path()) + '\\' + self.name) \
            if self.parent \
                else Path(getcwd())


    def get_abs_path(self):

        return self.path.absolute()


class DirectoryTree(Data):

    def __init__(self, name: str, parent: Data = None):

        super().__init__(name, parent)
        self.content = self.get_content()

    def __str__(self) -> str:

        return f'({self.name}; {list(map(str, self.content))})'

    def get_content(self) -> list[Data]:

        content = []

        for child in listdir(self.path):

            child_path = Path(str(self.path) + '\\' + child)

            if child_path.is_dir():
                content.append(DirectoryTree(child, self))
            else:
                content.append(File(child, self))

        return content

    def get_tree(self) -> str:

        result = self.parent.prefix + f'|--{fg(2)}{self.name}{fg(231)}' + '\n' \
            if self.parent \
                else fg(98) + self.name  + fg(231) + '\n'

        if self.content:
            for child in self.content:
                result += child.get_tree()

        return result


class File(Data):

    def __init__(self, name: str, parent: DirectoryTree):

        super().__init__(name, parent)

    def __str__(self):

        return self.name

    def get_tree(self):

        return self.parent.prefix + f'|--{fg(4)}{self.name}{fg(231)}' + '\n' \
            if self.parent \
                else f'|--{fg(4)}{self.name}{fg(231)}' + '\n'
