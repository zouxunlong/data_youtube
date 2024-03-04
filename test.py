from pytube import YouTube

yt = YouTube("https://www.youtube.com/watch?v=hTgaR2riBL8")
print("youtubeed", flush=True)
stream = yt.streams.filter(file_extension='mp4',resolution='360p').first()
print("streammed", flush=True)
stream.download("./", filename="hTgaR2riBL8.mp4")
print("downloaded", flush=True)


