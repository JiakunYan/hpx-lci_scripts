import sys
sys.path.append("../../include")
from platform_config_base import *

class PerlmutterConfig(PlatformConfigBase):
    name = "perlmutter"
    srun_pmi_option=""
    cpus_per_node = 64
    gpus_per_node = 4
    numa_policy = "default"
    account = "m4452"
    partition = "regular"
    
    @property
    def additional_sbatch_args(self):
        return ["--constraint=gpu"]

# def get_platform_config_all():
#     return {
#         "name": "perlmutter",
#         "core_num": 64,
#         "numa_policy": "default",
#     }