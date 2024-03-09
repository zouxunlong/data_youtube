import threading
from pytube import YouTube
import os
import time
import signal


class TimeoutError(Exception):
    pass

# Function to download a single video
def download_video(video_url, directory, filename):
     
    try:
        yt = YouTube(video_url)
        # stream_url = yt.streams.all()[0].url  # Get the URL of the video stream
        # stream = yt.streams.filter(file_extension='mp4',resolution='360p').first()
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(directory, filename=filename)
        print(f'downloaded video {video_url}, from dir{directory}')
        
    except Exception as e:
        print(f'error during downlading {e} for video url {video_url}')

# Function to download multiple videos with threading
def download_videos_from_list(file_path, directory, num_threads):

    error_ids = [line.split()[0] for line in open("./error_ids.log").readlines()]
    with open(file_path, 'r') as file:
        ids = file.readlines()

    # try:
    # Start threads to download videos
    threads = []
    for i, id in enumerate(ids):
        id = id.strip()  # Remove leading/trailing whitespace
        id = id.replace('\n','')

        if id in ["AccessDenie"]+error_ids:
            continue

        filename = '{}.wav'.format(id)
        if os.path.exists(os.path.join(directory, filename)):
            continue

        if len(id) < 20:
            video_url = 'https://www.youtube.com/watch?v=' + id
        
        thread = threading.Thread(target=download_video, args=(video_url, directory, filename))
        thread.start()
        threads.append(thread)

        
        try:
            if len(threads) >= num_threads:
                for t in threads:
                    t.join(timeout=2)
                if t.is_alive():
                    raise TimeoutError("Function execution exceeded 5 seconds")
                
                threads = []
        except Exception as e:
            print(f'exception during threading join in loop {e}')
            continue
            
        
    # Wait for remaining threads to finish
    for t in threads:
        t.join(timeout=5)
    threads = []
    # except Exception as e:
    #     print(f'error during threading------ {e}')
        
# Example usage
if __name__ == "__main__":
    # file_path = 'youtube_list.txt'  # Path to the file containing the list of YouTube video URLs
    # directory = './youtube/'  # Directory to save downloaded videos
    


    file_path = "./category-ids/08/081hv.txt"
    directory = "./jinyang/08/081hv"
    num_threads = 1  # Number of threads to use for downloading
    download_videos_from_list(file_path, directory, num_threads)

