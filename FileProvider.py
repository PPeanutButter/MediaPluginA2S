import os.path
import shutil


class FileProvider:

    def __init__(self):
        self.cache_dir = "tmp"
        self.convert_dir = "_convert"
        self.dst = []
        self.empty_cache()
        self.debug = False

    def empty_cache(self):
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        os.mkdir(self.cache_dir)
        if os.path.exists(self.convert_dir):
            shutil.rmtree(self.convert_dir)
        os.mkdir(self.convert_dir)

    def length(self):
        return len(self.getAssFiles()) + len(self.getSkipFiles())

    # mapping tmp/*.ass to _convert/*.srt
    def map(self, ass, post: str):
        dst = os.path.join(self.convert_dir, ass[len(self.cache_dir) + 1:-3] + post)
        self.dst.append(dst)
        return dst

    def getAssFiles(self) -> list:
        pass

    def getSkipFiles(self) -> list:
        pass

    def debug(self):
        self.debug = True

    def clean_up(self):
        if not self.debug:
            if os.path.exists(self.convert_dir):
                shutil.rmtree(self.convert_dir)
            if os.path.exists(self.cache_dir):
                shutil.rmtree(self.cache_dir)

    def __del__(self):
        self.clean_up()
