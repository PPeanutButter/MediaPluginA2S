import glob
import os.path
import sys
import zipfile

from FileProvider import FileProvider


class ZipProvider(FileProvider):

    def __init__(self, path):
        super().__init__()
        self.ass = []
        self.srt = []
        self.unzip_file(path)
        self.collect_files()

    def unzip_file(self, zip_src):
        r = zipfile.is_zipfile(zip_src)
        if r:
            fz = zipfile.ZipFile(zip_src, 'r')
            for file in fz.namelist():
                fz.extract(file, self.cache_dir)
        else:
            sys.exit(1)

    def collect_files(self):
        self.ass = glob.glob(os.path.join(self.cache_dir, "**/*.ass"), recursive=True)
        self.srt = glob.glob(os.path.join(self.cache_dir, "**/*.srt"), recursive=True)

    def getAssFiles(self):
        return self.ass

    def getSkipFiles(self):
        return self.srt
