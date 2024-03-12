import os
import time
from func_timeout import FunctionTimedOut, func_set_timeout
from pytube import YouTube


def remove_empty(dir):
    print("remove empty starts.", flush=True)
    for parent_dir, dirs, files in os.walk(dir):
        n=0
        dirs.sort()
        files.sort()
        for file in files:
            if os.path.getsize(os.path.join(parent_dir, file)) ==0:
                os.remove(os.path.join(parent_dir, file))
                n+=1
                continue
            if not file.endswith(".wav"):
                os.remove(os.path.join(parent_dir, file))
                n+=1
                continue
        print("complete {}, removed {}".format(parent_dir, n), flush=True)
    print("remove empty all completes.", flush=True)


def remove_forbidden(dir):
    print("remove forbidden starts.", flush=True)
    for parent_dir, dirs, files in os.walk(dir):
        n=0
        dirs.sort()
        files.sort()
        for file in files:
            if file.endswith(".errors"):
                lines=open(os.path.join(parent_dir, file)).readlines()
                lines=[line for line in lines if "Forbidden" not in line]
                open(os.path.join(parent_dir, file), "w").write("".join(lines))
                print("complete {}".format(os.path.join(parent_dir, file)), flush=True)
    print("remove forbidden all completes.", flush=True)


@func_set_timeout(60)
def download_video(id, directory, filename, error_file):
    try:
        video_url = 'https://www.youtube.com/watch?v={}'.format(id)
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(directory, filename=filename)
        print("DOWNLOADED: {} at {}".format(id, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), flush=True)
    except Exception as e:
        if "Forbidden" in str(e):
            os.remove(os.path.join(directory, filename))
            print("{} ERROR: {}".format(id, e), flush=True)
        else:
            print("{} ERROR: {}".format(id, e), flush=True)
            open(error_file, "a", encoding="utf8").write("{} ERROR: {}".format(id, e) + "\n")


def download(id, directory, filename, error_file):
    try:
        download_video(id, directory, filename, error_file)
    except FunctionTimedOut as e:
        print("{} ERROR: {}".format(id, e.msg.strip()), flush=True)
        open("./jumpped_ids.log", "a", encoding="utf8").write("{} ERROR: {}".format(id, e.msg.strip()) + "\n")

def count(dir):
    count_error=0
    count_ids=0
    for parent_dir, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".errors"):
                path=os.path.join(parent_dir, file)
                count_error+=len(open(path).readlines())
            if file.endswith(".txt"):
                path=os.path.join(parent_dir, file)
                count_ids+=len(open(path).readlines())
    print("{} : \n count_ids: {}, \n count_error: {}, \n should get: {}".format(dir, count_ids, count_error, count_ids-count_error), flush=True)

if __name__=="__main__":
    count("./category-ids/07")
