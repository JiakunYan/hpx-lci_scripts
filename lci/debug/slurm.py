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
from script_common_lci import *
from script_common import *

# load configuration
config_str = getenv_or("CONFIGS", None)
print(config_str)
config = json.loads(config_str)
print("Config: " + json.dumps(config))

if type(config) is list:
    configs = config
else:
    configs = [config]

pshell.run("export LCI_LOG_LEVEL=debug")
pshell.run("export LCT_LOG_LEVEL=debug")

start_time = time.time()
for config in configs:
    pshell.update_env(get_lci_environ_setting(config))

    cmd = (get_platform_config("get_srun_args", config) +
           get_platform_config("get_numactl_args", config) +
           config["args"])
    pshell.run(cmd)
end_time = time.time()
print("Executed {} configs. Total time is {}s.".format(len(configs), end_time - start_time))