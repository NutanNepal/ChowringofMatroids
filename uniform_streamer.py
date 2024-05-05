import subprocess
from multiprocessing import Pool

def execute_task(params):
    i, j = params
    command = f"sage UM_characters_decomposition.sage {i} {j}"
    #subprocess.run(command, shell=True)

def process_chunks(chunk):
    with Pool(processes=num_cores) as pool:
        pool.map(execute_task, chunk)

def chunk_combinations(combinations, chunk_size):
    for i in range(0, len(combinations), chunk_size):
        yield combinations[i:i + chunk_size]

if __name__ == '__main__':
    num_cores = 4

    combinations = [(i, j) for j in range(3, 12) for i in range(2, j)]

    chunk_size = len(combinations) // num_cores
    for chunk in chunk_combinations(combinations, chunk_size):
        process_chunks(chunk)