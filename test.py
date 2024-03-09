from pytube import YouTube
yt = YouTube("https://www.youtube.com/watch?v=EGa1umZbUtA")
print("youtubeed", flush=True)
stream = yt.streams.filter(only_audio=True).first()
print("streammed", flush=True)
stream.download("./", filename="EGa1umZbUtA.wav")
print("downloaded", flush=True)


# import time
# from func_timeout import FunctionTimedOut, func_set_timeout

# @func_set_timeout(1)
# def task(i):
#     try:
#         time.sleep(2)
#         print(i, flush=True)
#     except Exception as e:
#         print(e, flush=True)

# try:
#     task(1)
# except FunctionTimedOut as e:
#     print(e.msg.strip(), flush=True)
#     print(2, flush=True)
