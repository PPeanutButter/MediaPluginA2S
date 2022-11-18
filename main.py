import argparse
import os.path
import shutil
import subprocess
import sys
import zipfile

from AssProvider import AssProvider
from RarProvider import RarProvider
from SevenZipProvider import SevenZipProvider
from ZipProvider import ZipProvider


def zip_folder(_zip, name):
    files = os.listdir(name)
    for item in files:
        file_path = os.path.join(name, item)
        _zip.write(file_path, arcname=file_path.replace("_convert", ""))
        if os.path.isdir(file_path):
            zip_folder(_zip, file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='传入一个ass的文件、一个包含ass文件的压缩包')
    args = parser.parse_args()
    ext = str(args.path.split(".")[-1]).lower()
    if ext == 'ass':
        provider = AssProvider(args.path)
    elif ext == 'zip':
        provider = ZipProvider(args.path)
    elif ext == 'rar':
        provider = RarProvider(args.path)
    elif ext == '7z':
        provider = SevenZipProvider(args.path)
    else:
        sys.exit(1)
    for ass in provider.getAssFiles():
        srt = provider.map(ass)
        os.makedirs(srt[:-1*len(os.path.basename(srt))], exist_ok=True)
        result = subprocess.run([r"ffmpeg.exe", "-i", ass, srt], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
        print(result.decode())
    for srt in provider.getSkipFiles():
        shutil.copy(srt, provider.map(srt) + "_origin.srt")
    if os.path.exists("ass2srt.zip"):
        os.remove("ass2srt.zip")
    if provider.length() > 1:
        zip_folder(zipfile.ZipFile("ass2srt.zip", 'w', zipfile.ZIP_DEFLATED), provider.convert_dir)
