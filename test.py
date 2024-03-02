from pytube import YouTube

yt = YouTube("https://www.youtube.com/watch?v=-_dZ0AsLwmM")
stream = yt.streams.filter(file_extension='mp4',resolution='360p').first()
stream.download("./test", filename="JXsyX_Bmnv8.mp4")



# from concurrent.futures import ThreadPoolExecutor
# from multiprocessing import Pool, Manager
# import time

# def wait(pid, my_list):
#     time.sleep(3)
#     print("pid: {}, mylist_item: {}".format(pid, my_list.pop()),flush=True)

# def func(pid, my_list):

#     while my_list:
#         with ThreadPoolExecutor(max_workers=1) as pool:
#             for i in range(2):
#                 pool.submit(wait, pid, my_list)
#                 print("tasks for id: {} submitted.".format(i), flush=True)
#         print("one turn", flush=True)
#         time.sleep(3)


# if __name__ == '__main__':
#     manager = Manager()
#     my_list = manager.list()
#     my_list.extend([i for i in range(10)])
#     pool = Pool(processes=2)
#     for i in range(0, 2):
#         pool.apply_async(func, (i, my_list))
#     pool.close()
#     pool.join()

#     print(my_list, flush=True)

# import os

# for parent_dir, dirs, files in os.walk("./youtube8m"):
#     for file in files:
#         if os.path.getsize(os.path.join(parent_dir, file)) ==0:
#             os.remove(os.path.join(parent_dir, file))