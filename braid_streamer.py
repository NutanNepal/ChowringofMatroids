import subprocess
from multiprocessing import Pool

def execute_task(params):
    i = params
    command = f"sage braidMatroid_script.sage {i}"
    subprocess.run(command, shell=True)

def process_chunks(chunk):
    with Pool(processes=num_cores) as pool:
        pool.map(execute_task, chunk)

def chunk_combinations(combinations, chunk_size):
    for i in range(0, len(combinations), chunk_size):
        yield combinations[i:i + chunk_size]

if __name__ == '__main__':
    num_cores = 4

    combinations = [i for i in range(1, 8)]
    chunk_size = 1
    for chunk in chunk_combinations(combinations, chunk_size):
        process_chunks(chunk)