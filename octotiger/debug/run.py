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
    "name": "lci",
    "spack_env": "hpx-lcw",
    "nnodes": [256],
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
    # "in_buffer_assembly": 1,
    "match_table_type": "hashqueue",
    "cq_type": "array_atomic_faa",
    "reg_mem": 1,
    "ndevices": 2,
    "ncomps": 1,
    "lcw_backend": "mpi",
    "bg_work_when_send": 0,
    "bg_work_max_count": 32
}
matrix_outside = ["nnodes"]
matrix_inside = []
time_limit = 5

if platformConfig.name == "perlmutter":
    baseline["ntasks_per_node"] = 4
    baseline["ngpus"] = 1
    baseline["stop_step"] = 5
    # baseline["scenario"] = "dwd-l10-beginning"
    baseline["scenario"] = "dwd-l10-close_to_merger"

if platformConfig.name == "delta":
    baseline["spack_env"] = "hpx-lcw-sc24"
    baseline["nnodes"] = [2]
    baseline["ntasks_per_node"] = 1
    baseline["stop_step"] = 5
    baseline["griddim"] = 8
    # baseline["scenario"] = "dwd-l10-beginning"
    # baseline["scenario"] = "dwd-l10-close_to_merger"

if platformConfig.name == "polaris":
    baseline["spack_env"] = "hpx-lcw"
    baseline["nnodes"] = [4, 8, 16, 32]
    baseline["ntasks_per_node"] = 4
    baseline["ngpus"] = 1

if platformConfig.name == "rostam":
    baseline["spack_env"] = "hpx-lcw-openmpi"
    baseline["nnodes"] = [8]
    baseline["ntasks_per_node"] = 4

if platformConfig.name == "expanse":
    baseline["spack_env"] = "hpx-lcw-sc24-griddim2"
    baseline["nnodes"] = [32]
    baseline["griddim"] = 2
    baseline["nthreads"] = 16
    baseline["ntasks_per_node"] = 1

if platformConfig.name == "frontera":
    baseline["spack_env"] = "hpx-lcw-sc24"
    baseline["nnodes"] = [32]
    baseline["griddim"] = 8


configs = [
    # # # LCI v.s. MPI
    # {**baseline, "name": "mpi_a", "parcelport": "mpi", "sendimm": 1},
    # {**baseline, "name": "lci", "parcelport": "lci"},
    {**baseline, "name": "lci", "parcelport": "lci", "lock_mode": "global", "ndevices": 1},
    # {**baseline, "name": "lci_mutex", "parcelport": "lci", "cq_type": "array_mutex"},
    # {**baseline, "name": "lci_global", "parcelport": "lci", "lock_mode": "global"},
    # {**baseline, "name": "lci_global_b", "parcelport": "lci", "lock_mode": "global_b"},
    # {**baseline, "name": "lci_header_sync_single_poll", "ncomps": 2, "protocol": "sendrecv", "comp_type_header": "sync_single", "progress_type": "poll"},
    # {**baseline, "name": "lci_header_sync_single_nolock_poll", "ncomps": 2, "protocol": "sendrecv", "comp_type_header": "sync_single_nolock", "progress_type": "poll"},
    # {**baseline, "name": "lci", "parcelport": "lci", "protocol": "sendrecv"},
    # {**baseline, "name": "lci_sync_nolock", "parcelport": "lci", "protocol": "sendrecv", "comp_type_header": "sync_single_nolock"},
    # {**baseline, "name": "lci_sync", "parcelport": "lci", "protocol": "sendrecv", "comp_type_header": "sync_single"},
    # # completion type: followup
    # {**baseline, "name": "lci_followup_sync", "comp_type_followup": "sync"},
    # {**baseline, "name": "lci_rp", "progress_type": "rp"},
    # {**baseline, "name": "lci_pthread", "progress_type": "pthread"},
    # # ndevices + progress_type
    # {**baseline, "name": "lci_mt_d1_c1", "ndevices": 1, "progress_type": "worker", "ncomps": 1},
    # {**baseline, "name": "lci_mt_d2_c1", "ndevices": 2, "progress_type": "worker", "ncomps": 1},
    # {**baseline, "name": "lci_mt_d4_c1", "ndevices": 4, "progress_type": "worker", "ncomps": 1},
    # {**baseline, "name": "lci_pin_d1_c1", "ndevices": 1, "progress_type": "rp", "ncomps": 1},
    # {**baseline, "name": "lci_pin_d2_c1", "ndevices": 2, "progress_type": "rp", "ncomps": 1},
    # {**baseline, "name": "lci_pin_d4_c1", "ndevices": 4, "progress_type": "rp", "ncomps": 1},
]

if __name__ == "__main__":
    n = 1
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    mkdir_s("./run")

    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))

    for i in range(n):
        submit_jobs(configs, matrix_outside, matrix_inside, time=time_limit)