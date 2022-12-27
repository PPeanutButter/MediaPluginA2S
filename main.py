import argparse
import json
import os.path
import shutil
import subprocess
import sys
import threading
import time
import zipfile

from AssProvider import AssProvider
from RarProvider import RarProvider
from SevenZipProvider import SevenZipProvider
from ZipProvider import ZipProvider

convert_lock = threading.Semaphore(8)


def zip_folder(_zip, name):
    files = os.listdir(name)
    for item in files:
        file_path = os.path.join(name, item)
        _zip.write(file_path, arcname=file_path.replace("_convert", ""))
        if os.path.isdir(file_path):
            zip_folder(_zip, file_path)


def convert_mul_thread(_ass, _srt):
    try:
        subprocess.run([r"ffmpeg", "-i", _ass, _srt], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    finally:
        convert_lock.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='传入一个ass的文件、一个包含ass文件的压缩包')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    input_file_name = os.path.basename(args.path)
    output_file_name = input_file_name[:input_file_name.rfind(".")]+".zip"
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
        print(json.dumps(dict(code=-1, file="", files=[])))
        sys.exit(1)
    for ass in provider.getAssFiles():
        if convert_lock.acquire():
            srt = provider.map(ass, "srt")
            os.makedirs(srt[:-1*len(os.path.basename(srt))], exist_ok=True)
            threading.Thread(target=convert_mul_thread, args=(ass, srt,)).start()
    while True:
        # wait for all threads
        if convert_lock._value < 8:
            time.sleep(0.1)
        else:
            for srt in provider.getSkipFiles():
                shutil.copy(srt, provider.map(srt, "origin.srt"))
            if len(provider.dst) > 1:
                zip_folder(zipfile.ZipFile(output_file_name, 'w', zipfile.ZIP_DEFLATED), provider.convert_dir)
                print(json.dumps(dict(code=1, file=output_file_name, files=[os.path.basename(i) for i in provider.dst])))
            elif len(provider.dst) == 1:
                _name = os.path.basename(provider.dst[0])
                shutil.copy(provider.dst[0], _name)
                print(json.dumps(dict(code=2, file=_name, files=[os.path.basename(i) for i in provider.dst])))
            else:
                print(json.dumps(dict(code=-1, file="", files=[])))
            break
