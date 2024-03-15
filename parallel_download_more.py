from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Manager
import psutil
import os
from utils import download


def main(
        output_dir: str = "./audios_more",
        id_files_share: list[str] = [],
):
    while len(id_files_share)>0:

        id_file = id_files_share.pop()
        error_file=id_file.replace(".txt", ".errors")
        directory = os.path.join(output_dir, id_file.split("/")[-1].split(".")[0])
        if os.path.exists(error_file):
            error_ids = [line.split()[0] for line in open(error_file).readlines()]
        else:
            error_ids=[]

        print("tasks for id_file: {} started.".format(id_file), flush=True)

        with ThreadPoolExecutor(max_workers=4) as pool:
            for i, id in enumerate(open(id_file).readlines()):
                id = id.strip()

                if id in error_ids:
                    continue

                filename = '{}.wav'.format(id)
                if os.path.exists(os.path.join(directory, filename)):
                    continue

                pool.submit(download, id, directory, filename, error_file)
            print("tasks for id_file: {} submited.".format(id_file), flush=True)
        
        print("tasks for id_file: {} completed.".format(id_file), flush=True)


if __name__ == "__main__":

    open("./jumpped_ids.log", "w", encoding="utf8").write("")
    open("./pid2.log", "w", encoding="utf8").write(str(os.getpid())+" ")
    print("main process id {} starts.".format(os.getpid()), flush=True)

    output_dir = "./audios_more"
    id_file_dirs = ["./ids_more"]

    id_files=[]
    for id_file_dir in id_file_dirs:
        for parent_dir, dirs, files in os.walk(id_file_dir):
            for file in files:
                if file.endswith(".txt"):
                    id_files.append(os.path.join(parent_dir, file))
    id_files.sort()

    manager = Manager()
    id_files_share = manager.list()
    id_files_share.extend(id_files[30:])

    process_list = []

    for i in [96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127]:
        process = Process(target=main, args=(output_dir, id_files_share))
        process.start()
        process_list.append(process)
        p = psutil.Process(process.pid)
        p.cpu_affinity([i])
        print("process id {} starts on cpu {}".format(process.pid, i), flush=True)
        open("./pid2.log", "a", encoding="utf8").write(str(process.pid)+" ")

    for res in process_list:
        res.join()
    print("processes all finished.", flush=True)
