
import os

class FileManager:

    def __init__(self, pathto='.qtclang'):
        self.pathto = os.path.relpath(pathto)

    def exists(self):
        return os.path.exists(self.pathto)
    
    def create(self):
        # automatic closing
        with open(file=self.pathto, mode='w+') as f:
            pass

    def clear(self):
        self.create()

    def text(self):
        if not self.exists():
            return None
            # self.create()

        lines = None
        with open(file=self.pathto, mode='r') as f:
            lines = f.readlines()

        return lines

    def write(self, data, lines=False):
        with open(file=self.pathto, mode='a') as f:
            if not lines:
                f.write(str(data)+"\n")
            else:
                for line in data:
                    f.write(str(line)+"\n")


    