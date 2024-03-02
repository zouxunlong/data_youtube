from pytube import YouTube

yt = YouTube("https://www.youtube.com/watch?v=JXsyX_Bmnv8")
stream = yt.streams.filter(file_extension='mp4',resolution='360p').first()
stream.download("./test", filename="JXsyX_Bmnv8.mp4")