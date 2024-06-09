from script_common_lci import *

def get_lcw_environ_setting(config):
    ret = get_lci_environ_setting(config)
    if "lcw_backend" in config:
        ret["LCW_BACKEND_AUTO"] = config["lcw_backend"]
        if config["lcw_backend"] == "mpi":
            ret["MPIR_CVAR_CH4_GLOBAL_PROGRESS"] = 0
            if "ndevices" not in config:
                config["ndevices"] = 1
            if "use_stream" in config and config["use_stream"]:
                ret["MPIR_CVAR_CH4_RESERVE_VCIS"] = config["ndevices"]
                ret["LCW_MPI_USE_STREAM"] = 1
            else:
                ret["MPIR_CVAR_CH4_NUM_VCIS"] = config["ndevices"]
                ret["LCW_MPI_USE_STREAM"] = 0
            if "comp_type" in config:
                ret["LCW_MPI_COMP_TYPE"] = config["comp_type"]
        else:
            ret.update(get_lci_environ_setting(config))
    else:
        print("No LCW backend specified! Environment variables may not be specified correctly!")
    return ret
