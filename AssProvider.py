from FileProvider import FileProvider


class AssProvider(FileProvider):
    def __init__(self, path):
        super().__init__()
        self.ass = [path]

    def getAssFiles(self):
        return [self.ass]

    def getSkipFiles(self):
        return []
