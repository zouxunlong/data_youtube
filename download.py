
from pytube import YouTube

def download_video(video_url, directory, filename):
    try:
        yt = YouTube(video_url)
        print(f"youtubeed:{filename}", flush=True)
        stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('bitrate').last()
        print(f"streammed:{filename}", flush=True)
        stream.download(directory, filename=filename)
        print(f"downloaded:{filename}", flush=True)
    except Exception as e:
        print('error during downloading {}: {}'.format(filename, e), flush=True)


def download_videos_from_list(file_path, directory):
    with open(file_path, 'r') as file:
        video_urls = file.readlines()
    try:
        for i, video_url in enumerate(video_urls):
            video_url = video_url.strip()  # Remove leading/trailing whitespace
            video_url = video_url.replace('\n','')
            if len(video_url) < 20:
                video_url = 'https://www.youtube.com/watch?v=' + video_url
            filename = video_url.split('watch?v=')[-1] + '.mp4'
            download_video(video_url, directory, filename)
    except:
        print('error during threading', flush=True)
        

if __name__ == "__main__":
    
    file_path = "./category-ids/0cvq3.txt"
    directory = "./jinyang/0cvq3"

    download_videos_from_list(file_path, directory)