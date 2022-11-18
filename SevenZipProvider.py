from py7zr import SevenZipFile

from ZipProvider import ZipProvider


class SevenZipProvider(ZipProvider):

    def __init__(self, path):
        super().__init__(path)

    def unzip_file(self, zip_src):
        with SevenZipFile(zip_src, 'r') as z:
            z.extractall(path=self.cache_dir)
