#!/usr/bin/env python3

import os
import sys
import shutil
import copy
import json
sys.path.append("../../include")
from script_common import *
import time

baseline = {
    "name": "pingpong",
    "spack_env": "hpx-lcw",
    "nnodes": [2],
    "ntasks_per_node": 1,
    "args": ["lci_hello_world"],
    # "args": ["pingpong_performance2", "--nchains=1024", "--nsteps=10000", "--batch-size=5"],
    "parcelport": "lci",
    "protocol": "putsendrecv",
    "comp_type": "queue",
    "progress_type": "worker",
    "prg_thread_num": "auto",
    "sendimm": 1,
    "backlog_queue": 0,
    "prepost_recv_num": 1,
    "zero_copy_recv": 1,
    "agas_caching": 0,
    # "in_buffer_assembly": 1,
    "match_table_type": "hashqueue",
    "cq_type": "array_atomic_faa",
    "reg_mem": 1,
    "ndevices": 1,
    "ncomps": 1,
    "lcw_backend": "mpi"
}
matrix_outside = ["nnodes"]
matrix_inside = []
time_limit = 1

configs = [
    # baseline,
    {**baseline, "name": "lci"},
    # {**baseline, "name": "mpi-nbytes", "parcelport": "mpi"},
    # {**baseline, "name": "lcw_mpi-nbytes", "parcelport": "lcw"},
]

if __name__ == "__main__":
    n = 1
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    mkdir_s("./run")

    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))

    for i in range(n):
        submit_jobs(configs, matrix_outside, matrix_inside, config_fn=None, time=time_limit)