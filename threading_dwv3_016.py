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
    with open(file_path, 'r') as file:
        video_urls = file.readlines()
        
    # try:
    # Start threads to download videos
    threads = []
    for i, video_url in enumerate(video_urls):
        video_url = video_url.strip()  # Remove leading/trailing whitespace
        video_url = video_url.replace('\n','')
        if len(video_url) < 20:
            video_url = 'https://www.youtube.com/watch?v=' + video_url
        # filename = f'video_{i + 1}.mp4'
        # filename = video_url.split('watch?v=')[-1] + '.mp4'
        filename = video_url.split('watch?v=')[-1] + '.wav'
        
        thread = threading.Thread(target=download_video, args=(video_url, directory, filename))
        thread.start()
        threads.append(thread)
        print(f'handling url-------start: {video_url},len of threads {len(threads)}')
        check = 0
        # Limit the number of active threads
        # print(len(threads),'get the len of threading')
        
        try:
            if len(threads) >= num_threads:
                for t in threads:
                    t.join(timeout=5)
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
    
    download_path = './youtube8m_v1_016'
    id_file_path = './category-ids_v1_016'
    file_path = ''
    directory = ''
    for num,file in enumerate(os.listdir(id_file_path)):
        if file.endswith('txt'):
            file_path = os.path.join(id_file_path,file)
            directory = os.path.join(download_path,file.split('.')[0])
            num_threads = 16  # Number of threads to use for downloading
            download_videos_from_list(file_path, directory, num_threads)
        else:
            print(f'file not txt {file}')
