import glob
import os.path
import subprocess
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
        subprocess.run([r"unzip", zip_src, "-d", self.cache_dir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def collect_files(self):
        self.ass = glob.glob(os.path.join(self.cache_dir, "**/*.ass"), recursive=True)
        self.srt = glob.glob(os.path.join(self.cache_dir, "**/*.srt"), recursive=True)

    def getAssFiles(self):
        return self.ass

    def getSkipFiles(self):
        return self.srt
