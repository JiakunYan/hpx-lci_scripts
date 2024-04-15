import sys

sys.path.append("../../include")
from platform_config_base import *

class ExpanseConfig(PlatformConfigBase):
    name = "expanse"
    network = "ibv"
    cpus_per_node = 128
    gpus_per_node = 0
    numa_policy = "default"
    # account = None
    partition = "compute"
    additional_sbatch_args = ["--mem=128G", "--constraint=\"lustre\""]
    scenarios_path = {
        "rs": "%root%/octotiger/data",
    }

    def get_srun_args(self, config):
        if "parcelport" not in config:
            srun_pmi_option = ["--mpi=pmi2"]
        elif config["parcelport"] == "lci":
            srun_pmi_option = ["--mpi=pmi2"]
        else:
            srun_pmi_option = ["--mpi=pmix"]
        return ["srun"] + srun_pmi_option

