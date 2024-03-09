from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Manager
import psutil
import os
from utils import remove_empty, download


def main(
        output_dir: str = "./youtube8m",
        id_files_share: list[str] = [],
        error_ids: list[str] = [],
):
    while len(id_files_share)>0:

        id_file = id_files_share.pop()
        directory = os.path.join(output_dir, id_file.split('/')[-1].split(".")[0])

        print("tasks for id_file: {} started.".format(id_file), flush=True)

        with ThreadPoolExecutor(max_workers=4) as pool:
            for i, id in enumerate(open(id_file).readlines()):
                id = id.strip()

                if id in ["AccessDenie"] + error_ids:
                    continue

                filename = '{}.wav'.format(id)
                if os.path.exists(os.path.join(directory, filename)):
                    continue

                pool.submit(download, id, directory, filename)
            print("tasks for id_file: {} submited.".format(id_file), flush=True)
        
        print("tasks for id_file: {} completed.".format(id_file), flush=True)


if __name__ == "__main__":

    remove_empty("./youtube8m")

    print("main process id {} starts.".format(os.getpid()), flush=True)
    open("./pid.log", "w", encoding="utf8").write(str(os.getpid())+" ")
    output_dir = "./youtube8m/09"
    id_file_dir = "./category-ids/09"
    id_files = os.listdir(id_file_dir)
    id_files.sort()
    id_files = [os.path.join(id_file_dir, id_file) for id_file in id_files]
    error_ids = [line.split()[0] for line in open("./error_ids.log").readlines()]

    manager = Manager()
    id_files_share = manager.list()
    id_files_share.extend(id_files)

    num_cpus = os.cpu_count()
    process_list = []

    for i in [i for i in range(17)]:
        process = Process(target=main, args=(output_dir, id_files_share, error_ids))
        process.start()
        process_list.append(process)
        p = psutil.Process(process.pid)
        p.cpu_affinity([i])
        print("process id {} starts on cpu {}".format(process.pid, i), flush=True)
        open("./pid.log", "a", encoding="utf8").write(str(process.pid)+" ")

    for res in process_list:
        res.join()
    print("processes all finished.", flush=True)
