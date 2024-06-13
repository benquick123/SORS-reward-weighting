import os
from time import sleep
from datetime import datetime
import numpy as np
import multiprocessing as mp


def run_command(command):
    print("running command:", command)
    os.system(command)
    print("end command:", command)


if __name__ == "__main__":
    
    envs = ["ant", "halfcheetah", "hopper", "humanoid", "swimmer", "walker2d"]
    seeds = np.arange(0, 10, 1)
    log_path = "/home/benjamin/SORS/results/original_results"
    commands = [
        # "python -m SORS.scripts.sors --seed %d --log_dir %s --config_file ./SORS/experiments/sors.gin ./SORS/experiments/envs/delayed_%s.gin",
        "python -m SORS.scripts.sors --seed %d --log_dir %s --config_file ./SORS/experiments/sors.gin ./SORS/experiments/envs/end_%s.gin",
        # "python -m SORS.scripts.offpolicy_rl --seed %d --log_dir %s --config_file ./SORS/experiments/sac.gin ./SORS/experiments/envs/delayed_%s.gin",
        # "python -m SORS.scripts.offpolicy_rl --seed %d --log_dir %s --config_file ./SORS/experiments/sac.gin ./SORS/experiments/envs/%s.gin"
    ]
    command_types = ["sors", "sac_baseline", "gt_reward"]
    
    processes = []
    max_processes = 6
    
    for seed in seeds:
        for env in envs:
            for command_name, command in zip(command_types, commands):
                log_dir = str(datetime.now()).split(".")[0].replace(":", "-").replace(" ", "_") + "_" + env + "_" + str(seed) + "_" + command_name
                command_to_run = command % (seed, os.path.join(log_path, log_dir), env)
                
                p = mp.Process(target=run_command, args=[command_to_run])
                p.start()
                processes.append(p)
                sleep(1)
                
                if len(processes) == max_processes:
                    for p in processes:
                        p.join()
                    processes = []
                
                sleep(1)
                
    for p in processes:
        p.join()