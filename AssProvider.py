import os

from FileProvider import FileProvider


class AssProvider(FileProvider):
    def __init__(self, path):
        super().__init__()
        self.ass = path

    def map(self, ass, post: str):
        dst = os.path.join(self.convert_dir, os.path.basename(ass)[:-3] + post)
        self.dst.append(dst)
        return dst

    def getAssFiles(self):
        return [self.ass]

    def getSkipFiles(self):
        return []
