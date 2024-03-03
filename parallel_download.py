from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Manager
from pytube import YouTube
import psutil
import os


def download_video(video_url, directory, filename):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(
            file_extension='mp4', resolution='360p').first()
        stream.download(directory, filename=filename)
        # print(f"downloaded:{filename}", flush=True)
    except Exception as e:
        print('error {} during downloading {}'.format(e, video_url), flush=True)
        open("./error_urls.log", "a", encoding="utf8").write(video_url+"\n")


def main(
        output_dir: str = "./youtube8m",
        id_files_share: list[str] = [],
        error_urls: list[str] = [],
):
    while id_files_share:

        id_file = id_files_share.pop()
        directory = os.path.join(output_dir, id_file.split('/')[-1].split(".")[0])

        with ThreadPoolExecutor(max_workers=20) as pool:

            for id in open(id_file).readlines():
                id = id.strip()
                if id in ["AccessDenie"]:
                    continue

                video_url = 'https://www.youtube.com/watch?v=' + id
                if video_url in error_urls:
                    continue

                filename = '{}.mp4'.format(id)
                if os.path.exists(os.path.join(directory, filename)):
                    continue

                pool.submit(download_video, video_url, directory, filename)

            print("tasks for id_file: {} submitted.".format(id_file), flush=True)


if __name__ == "__main__":
    print("main process id {} starts.".format(os.getpid()), flush=True)
    open("./pid.log", "w", encoding="utf8").write(str(os.getpid())+" ")

    output_dir = "./youtube8m"
    id_file_dir = "./category-ids"
    id_files = os.listdir(id_file_dir)
    id_files.sort(reverse=True)
    id_files = [os.path.join(id_file_dir, id_file) for id_file in id_files][50:100]

    thunder5_list=id_files[:50]
    thunder1_list=id_files[50:100]
    thunder8_list=id_files[100:150]
    thunder7_list=id_files

    manager = Manager()
    id_files_share = manager.list()
    id_files_share.extend(id_files)

    error_urls = [url.strip() for url in open("./error_urls.log").readlines()]

    num_cpus = os.cpu_count()
    process_list = []

    for i in [i for i in range(10)]:
        process = Process(target=main, args=(output_dir, id_files_share, error_urls))
        process.start()
        process_list.append(process)
        p = psutil.Process(process.pid)
        p.cpu_affinity([i])
        print("process id {} starts on cpu {}".format(process.pid, i), flush=True)
        open("./pid.log", "a", encoding="utf8").write(str(process.pid)+" ")

    for res in process_list:
        res.join()
    print("processes all finished.", flush=True)
