#!/usr/bin/env python3

import os
import sys
import shutil
import copy
import json
sys.path.append("../../include")
from script_common import *

baseline = {
    "name": "lci",
    "spack_env": "hpx-lci-sc24-adae",
    "nnodes": [32],
    "ntasks_per_node": 1,
    "griddim": 8,
    "max_level": 5,
    "stop_step": 5,
    "zc_threshold": 8192,
    "scenario": "rs",
    "parcelport": "lci",
    "protocol": "putsendrecv",
    "comp_type_header": "queue",
    "comp_type_followup": "queue",
    "progress_type": "worker",
    "prg_thread_num": "auto",
    "sendimm": 1,
    "backlog_queue": 0,
    "prepost_recv_num": 1,
    "zero_copy_recv": 1,
    "in_buffer_assembly": 1,
    "match_table_type": "hashqueue",
    "cq_type": "array_atomic_faa",
    "reg_mem": 1,
    "ndevices": 2,
    "ncomps": 1,
}
matrix_outside = ["nnodes"]
matrix_inside = []
time_limit = 1

if platformConfig.name == "expanse":
    baseline["ntasks_per_node"] = 2
if platformConfig.name == "delta":
    baseline["ntasks_per_node"] = 2

configs1 = [
    # LCI v.s. MPI
    {**baseline, "name": "lci", "nnodes": [2, 4, 8, 16, 32], "parcelport": "lci"},
    {**baseline, "name": "mpi_a", "nnodes": [2, 4, 8, 16, 32], "parcelport": "mpi", "sendimm": 0},
    {**baseline, "name": "mpi", "nnodes": [2, 4, 8, 16, 32], "parcelport": "mpi", "sendimm": 1},
]

configs2 = [
    # LCI v.s. MPI
    # communication prototype
    {**baseline, "name": "lci_2queue", "ncomps": 2},
    {**baseline, "name": "lci_sendrecv", "ncomps": 2, "protocol": "sendrecv"},
    {**baseline, "name": "lci_sendcrecv", "protocol": "sendrecv", "enable_sendmc": 1},
    # completion type: header
    {**baseline, "name": "lci_header_sync_single", "ncomps": 2, "protocol": "sendrecv", "comp_type_header": "sync_single"},
    {**baseline, "name": "lci_header_sync_single_nolock", "ncomps": 2, "protocol": "sendrecv", "comp_type_header": "sync_single_nolock"},
    # completion type: followup
    {**baseline, "name": "lci_followup_queue_mutex", "cq_type": "array_mutex", "enable_sendmc": 1},
    {**baseline, "name": "lci_followup_sync", "comp_type_followup": "sync", "enable_sendmc": 1},
    {**baseline, "name": "lci_followup_2queue", "ncomps": 2, "enable_sendmc": 1},
    # # progress type
    {**baseline, "name": "lci_pin", "progress_type": "rp"},
    {**baseline, "name": "lci_pthread", "progress_type": "pthread"},
    {**baseline, "name": "lci_pthread_worker", "progress_type": "pthread_worker"},
    {**baseline, "name": "lci_pthread_d1", "progress_type": "pthread", "ndevices": 1},
    {**baseline, "name": "lci_pthread_worker_d1", "progress_type": "pthread_worker", "ndevices": 1},
    # # device lock
    {**baseline, "name": "lci_global_d1", "ndevices": 1, "parcelport": "lci", "lock_mode": "global"},
    {**baseline, "name": "lci_global_d2", "ndevices": 2, "parcelport": "lci", "lock_mode": "global"},
    {**baseline, "name": "lci_global_d4", "ndevices": 4, "parcelport": "lci", "lock_mode": "global"},
    {**baseline, "name": "lci_global_d8", "ndevices": 8, "parcelport": "lci", "lock_mode": "global"},
    {**baseline, "name": "lci_global_b_d1", "ndevices": 1, "parcelport": "lci", "lock_mode": "global_b"},
    {**baseline, "name": "lci_global_b_d2", "ndevices": 2, "parcelport": "lci", "lock_mode": "global_b"},
    {**baseline, "name": "lci_global_b_d4", "ndevices": 4, "parcelport": "lci", "lock_mode": "global_b"},
    {**baseline, "name": "lci_global_b_d8", "ndevices": 8, "parcelport": "lci", "lock_mode": "global_b"},
    # ndevices + progress_type
    {**baseline, "name": "lci_mt_d1_c1", "ndevices": 1, "progress_type": "worker", "ncomps": 1},
    {**baseline, "name": "lci_mt_d2_c1", "ndevices": 2, "progress_type": "worker", "ncomps": 1},
    {**baseline, "name": "lci_mt_d4_c1", "ndevices": 4, "progress_type": "worker", "ncomps": 1},
    {**baseline, "name": "lci_mt_d8_c1", "ndevices": 8, "progress_type": "worker", "ncomps": 1},
    {**baseline, "name": "lci_pin_d1_c1", "ndevices": 1, "progress_type": "rp", "ncomps": 1},
]

if __name__ == "__main__":
    mode = "mpi_vs_lci"
    n = 1
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    if len(sys.argv) > 2:
        n = int(sys.argv[2])
    if mode == "config":
        print("use mode config")
        configs = configs2
    else:
        print("use mode mpi_vs_lci")
        configs = configs1

    mkdir_s("./run")

    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))

    for i in range(n):
        submit_jobs(configs, matrix_outside, matrix_inside, time=time_limit)