import os
import time
from func_timeout import FunctionTimedOut, func_set_timeout
from pytube import YouTube


def remove_empty(dir):
    for parent_dir, dirs, files in os.walk(dir):
        for file in files:
            if os.path.getsize(os.path.join(parent_dir, file)) ==0:
                os.remove(os.path.join(parent_dir, file))



@func_set_timeout(60)
def download_video(id, directory, filename, error_file):
    try:
        video_url = 'https://www.youtube.com/watch?v={}'.format(id)
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(directory, filename=filename)
        print("DOWNLOADED: {} at {}".format(id, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), flush=True)
    except Exception as e:
        print("{} ERROR: {}".format(id, e), flush=True)
        open(error_file, "a", encoding="utf8").write("{} ERROR: {}".format(id, e) + "\n")


def download(id, directory, filename, error_file):
    try:
        download_video(id, directory, filename, error_file)
    except FunctionTimedOut as e:
        print("{} ERROR: {}".format(id, e.msg.strip()), flush=True)
        open("./jumpped_ids.log", "a", encoding="utf8").write("{} ERROR: {}".format(id, e.msg.strip()) + "\n")

def count(dir):
    count=0
    for parent_dir, dirs, files in os.walk(dir):
        for file in files:
            path=os.path.join(parent_dir, file)
            num=len(open(path).readlines())
            count+=num
    print(count, flush=True)

if __name__=="__main__":
    remove_empty("./youtube8m")
