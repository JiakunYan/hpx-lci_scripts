from package_configs.package_config_base import *


class PackageConfigLcw(PackageConfigBase):
    name = "lcw"

    def get_dependency(self, config):
        if "lcw:backend" in config:
            if config["lcw:backend"] == "mpi":
                return ["mpich"]
            else:
                return ["lci"]
        else:
            return ["lci"]

    def get_default_config(self, config):
        default = {
            "lcw:backend": "mpi",
            "lcw:use_stream": 0,
            "lcw:comp_type": "cont",
        }
        set_config_if_not_exist(config, default)
        return config

    def get_env_vars(self, config):
        ret = {}
        set_env_if_exist(ret, "LCW_BACKEND_AUTO", config, "lcw:backend")
        set_env_if_exist(ret, "LCW_MPI_USE_STREAM", config, "lcw:use_stream")
        set_env_if_exist(ret, "LCW_MPI_COMP_TYPE", config, "lcw:comp_type")
        return ret

    def get_args(self, config):
        args = []
        return args


register_package(PackageConfigLcw())