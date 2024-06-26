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
    "spack_env": "hpx-mpich",
    "nnodes": [32],
    "ntasks_per_node": 2,
    "ot:griddim": 8,
    "ot:max_level": 5,
    "ot:stop_step": 20,
    "ot:scenario": "rs",
    "hpx:parcelport": "lci",
    "hpx:zc_threshold": 8192,
    "hpx:protocol": "putsendrecv",
    "hpx:progress_type": "worker",
    "hpx:prg_thread_num": "auto",
    "hpx:sendimm": 1,
    "hpx:backlog_queue": 0,
    "hpx:prepost_recv_num": 1,
    "hpx:zero_copy_recv": 1,
    "hpx:reg_mem": 1,
    "hpx:ndevices": 2,
    "hpx:ncomps": 1,
    "lcw:backend": "mpi",
    "lci:match_table_type": "hashqueue",
    "lci:cq_type": "array_atomic_faa",
}
matrix_outside = ["nnodes"]
matrix_inside = []
time_limit = 1

if platformConfig.name == "rostam":
    baseline["spack_env"] = "hpx-mpich-ofi"
    baseline["nnodes"] = [12]
if platformConfig.name == "polaris":
    baseline["spack_env"] = "hpx-mpich"
    baseline["nnodes"] = [8]
    baseline["ntasks_per_node"] = 1
if platformConfig.name == "expanse":
    baseline["spack_env"] = "hpx-mpich-ofi"

configs = [
    # # # LCI v.s. MPI
    # {**baseline, "name": "mpi_a", "parcelport": "mpi", "sendimm": 0},
    # {**baseline, "name": "mpi", "parcelport": "mpi"},
    # {**baseline, "name": "lci", "parcelport": "lci"},
    # {**baseline, "name": "lci-ibv", "parcelport": "lci", "spack_env": "hpx-mpich"},
    # {**baseline, "name": "lcw_lci", "parcelport": "lcw", "lcw_backend": "lci"},
    # {**baseline, "name": "lcw_cont_d2", "parcelport": "lcw", "comp_type": "cont"},
    # {**baseline, "name": "lcw_req_d2", "parcelport": "lcw", "comp_type": "req"},
    # {**baseline, "name": "lcw_cont_d1", "parcelport": "lcw", "comp_type": "cont", "ndevices": 1},
    # {**baseline, "name": "lcw_req_d1", "parcelport": "lcw", "comp_type": "req", "ndevices": 1},
    # {**baseline, "name": "lcw_cont_d4", "parcelport": "lcw", "comp_type": "cont", "ndevices": 4},
    # {**baseline, "name": "lcw_req_d4", "parcelport": "lcw", "comp_type": "req", "ndevices": 4},
    {**baseline, "name": "lcw_cont_d2_s", "parcelport": "lcw", "comp_type": "cont", "use_stream": 1},
    {**baseline, "name": "lcw_cont_d1_s", "parcelport": "lcw", "comp_type": "cont", "ndevices": 1, "use_stream": 1},
    {**baseline, "name": "lcw_cont_d4_s", "parcelport": "lcw", "comp_type": "cont", "ndevices": 4, "use_stream": 1},
]

if __name__ == "__main__":
    n = 1
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    mkdir_s("./run")

    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))

    for i in range(n):
        submit_jobs(configs, matrix_outside, matrix_inside, time=time_limit)