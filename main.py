import argparse
import json
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
        print(json.dumps(dict(code=-1, file="")))
        sys.exit(1)
    for ass in provider.getAssFiles():
        srt = provider.map(ass, "srt")
        os.makedirs(srt[:-1*len(os.path.basename(srt))], exist_ok=True)
        subprocess.run([r"ffmpeg", "-i", ass, srt], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for srt in provider.getSkipFiles():
        shutil.copy(srt, provider.map(srt, "origin.srt"))
    if os.path.exists("ass2srt.zip"):
        os.remove("ass2srt.zip")
    if len(provider.dst) > 1:
        zip_folder(zipfile.ZipFile("ass2srt.zip", 'w', zipfile.ZIP_DEFLATED), provider.convert_dir)
        print(json.dumps(dict(code=1, file="ass2srt.zip", files=[os.path.basename(i) for i in provider.dst])))
    elif len(provider.dst) == 1:
        shutil.copy(provider.dst[0], "ass2srt.srt")
        print(json.dumps(dict(code=2, file="ass2srt.srt", files=[os.path.basename(i) for i in provider.dst])))
    else:
        print(json.dumps(dict(code=-1, file="")))
