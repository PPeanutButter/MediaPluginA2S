import subprocess

from ZipProvider import ZipProvider


class RarProvider(ZipProvider):

    def __init__(self, path):
        super().__init__(path)

    def unzip_file(self, zip_src):
        subprocess.run([r"D:\Program Files (x86)\WinRAR\Rar.exe", "x", zip_src, self.cache_dir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
