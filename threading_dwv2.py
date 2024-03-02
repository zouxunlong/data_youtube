from concurrent.futures import ThreadPoolExecutor
from pytube import YouTube
import os


def download_video(video_url, directory, filename):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(file_extension='mp4',resolution='360p').first()
        stream.download(directory, filename=filename)
        print(f"downloaded:{filename}")
    except:
        print('error during downloading {}'.format(video_url), flush=True)


def download_videos_from_list(id_file_path, directory, num_threads):

    ids = open(id_file_path).readlines()

    with ThreadPoolExecutor(max_workers=num_threads) as pool:
        for id in ids:
            id = id.strip()
            if id in ["AccessDenie"]:
                continue
            video_url = 'https://www.youtube.com/watch?v=' + id
            filename = '{}.mp4'.format(id)
            pool.submit(download_video, video_url, directory, filename)
            print('task for {} submitted.....'.format(video_url), flush=True)


# Example usage
if __name__ == "__main__":
    
    output_dir = './youtube8m'
    id_file_dir = './category-ids'
    id_files=os.listdir(id_file_dir)
    id_files.sort()
    for i, id_file in enumerate(id_files[:70]):

        id_file_path = os.path.join(id_file_dir,id_file)
        directory = os.path.join(output_dir, id_file.split('.')[0])

        download_videos_from_list(id_file_path, directory, num_threads = 20)

        print("complete {}th id_file {}".format(i+1, id_file), flush=True)