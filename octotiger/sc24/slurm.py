#!/usr/bin/env python3
import os
import sys
import json
import time

# load root path
current_path = os.environ["CURRENT_PATH"]
root_path = os.path.realpath(os.path.join(current_path, "../.."))

sys.path.append(os.path.join(root_path, "include"))
import pshell
from script_common_octotiger import *
from script_common import *

# load configuration
config_str = getenv_or("CONFIGS", get_octotiger_default_config())
print(config_str)
config = json.loads(config_str)

if type(config) is list:
    configs = config
else:
    configs = [config]

if platformConfig.name == "expanse":
    # We need to following environment variables to make sure UCX is not super slow.
    # (Apparently, UCX's auto TLS selection and multi-raid optimizations will run into performance issues on Expanse)
    pshell.run("export UCX_TLS=rc,self")
    pshell.run("export UCX_MAX_RNDV_RAILS=1")
    pshell.run("export UCX_NET_DEVICES=mlx5_0:1")
    # We need to following environment variables to configure UCX to use the same communication protocol as LCI.
    pshell.run("export UCX_BCOPY_THRESH=32")
    pshell.run("export UCX_RNDV_THRESH=12288")

start_time = time.time()
for config in configs:
    print("Config: " + json.dumps(config))
    pshell.update_env(get_octotiger_environ_setting(config))

    scenario = "rs"
    if "scenario" in config:
        scenario = config["scenario"]
    scenarios_path = get_platform_config("scenarios_path", config)[scenario].replace("%root%", root_path)
    pshell.run(f"cd {scenarios_path}")

    cmd = (get_platform_config("get_srun_args", config) + ["-u"] +
           get_platform_config("get_numactl_args", config) +
           get_octotiger_cmd(config))
    pshell.run(cmd)
end_time = time.time()
print("Executed {} configs. Total time is {}s.".format(len(configs), end_time - start_time))