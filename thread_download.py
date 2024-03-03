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
        print(f"downloaded:{filename}", flush=True)
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

        with ThreadPoolExecutor() as pool:

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
    id_files = [os.path.join(id_file_dir, id_file) for id_file in id_files]

    list_thunder5=id_files[:50]
    list_thunder1=id_files[50:100]
    list_thunder8=id_files[100:150]
    list_demo2=id_files[150:200]
    list_thunder7=id_files[200:]

    error_urls = [url.strip() for url in open("./error_urls.log").readlines()]

    main(output_dir="./youtube8m",
         id_files_share=list_thunder1,
         error_urls=error_urls
         )

    print("all finished.", flush=True)
