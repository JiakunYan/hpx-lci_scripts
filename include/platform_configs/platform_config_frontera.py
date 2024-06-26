import sys
sys.path.append("../../include")
from platform_config_base import *
import pshell

class FronteraConfig(PlatformConfigBase):
    name = "frontera"
    network = "ibv"
    cpus_per_node = 56
    gpus_per_node = 0
    numa_policy = "default"
    account = "CCR23056"
    scenarios_path = {
        "rs": "%root%/octotiger/data",
        "dwd-l10-close_to_merger": "/work2/07620/tg869200/frontera/octotiger/q07_l10/close_to_merger",
        "dwd-l10-close_to_merger-workspace": "/work2/07620/tg869200/frontera/octotiger/q07_l10/close_to_merger-workspace"
    }

    def partition(self, config):
        nnodes = config["nnodes"]
        # if nnodes <= 40:
        #     ret, _ = pshell.run(["squeue", "-u", os.environ["USER"]], to_print=False)
        #     count = ret.count("development")
        #     if count <= 2:
        #         return "development"
        if nnodes == 1:
            return "flex"
        elif nnodes == 2:
            return "small"
        elif nnodes <= 512:
            return "normal"
        else:
            return "prod"

    def get_srun_args(self, config):
        return ["srun", "--mpi=pmi2"]

    def custom_env(self, config):
        return {"I_MPI_PMI_VALUE_LENGTH_MAX": "512"}

