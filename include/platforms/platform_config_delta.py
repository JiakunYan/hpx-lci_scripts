import sys
sys.path.append("../../include")
from platform_config_base import *

class DeltaConfig(PlatformConfigBase):
    name = "delta"
    network = "ss11"
    cpus_per_node = 128
    gpus_per_node = 0
    cpus_per_core = 1
    numa_policy = "default"
    # account = None
    partition = "cpu"
    qos = None
    scenarios_path = {
        "rs": "%root%/octotiger/data",
    }

    @property
    def additional_sbatch_args(self):
        return []

    def get_srun_args(self, config):
        return ["srun"]

    def custom_env(self, config):
        return {"FI_CXI_RX_MATCH_MODE": "software"}

