#!/usr/bin/env python3
import os
import sys
import json
import time

# load root path
current_path = os.environ["CURRENT_PATH"]
root_path = os.path.realpath(os.path.join(current_path, "../.."))

sys.path.append(os.path.join(root_path, "include"))
from script_common import *

# load configuration
config_str = getenv_or("CONFIGS", None)
print(config_str)
config = json.loads(config_str)

if type(config) is list:
    configs = config
else:
    configs = [config]

# pshell.run("export LCI_LOG_LEVEL=debug")
# pshell.run("export LCT_LOG_LEVEL=debug")
# pshell.run("export LCI_OFI_PROVIDER_HINT=\"udp\"")
# pshell.run("export HPX_LCI_LOG_LEVEL=debug")
# pshell.run("export LCT_PMI_BACKEND=pmi2")
# pshell.run("export LCT_PCOUNTER_MODE=on-the-fly")
# pshell.run("export LCT_PCOUNTER_AUTO_DUMP=stderr")
# pshell.run("ulimit -c unlimited")
# pshell.run("export LCI_ENABLE_PRG_NET_ENDPOINT=0")
# pshell.run("export LCI_PAPI_EVENTS=PAPI_FP_OPS")
# pshell.run("export FI_LOG_LEVEL=debug")
# pshell.run("export FI_LOG_PROV=cxi")
# pshell.run("export MPIR_CVAR_CH4_NUM_VCIS=10")
pshell.run("export UCX_TLS=rc_v,self")
# pshell.run("export UCX_RNDV_THRESH=12288")
# pshell.run("export UCX_MAX_RNDV_RAILS=1")
# pshell.run("export UCX_BCOPY_THRESH=32")
# pshell.run("export UCX_NET_DEVICES=mlx5_0:1")
# pshell.run("export LCW_LOG_LEVEL=info")
# pshell.run("export LCW_FORCE_PTHREAD_SPINLOCK=1")
# pshell.run("export LCW_MPI_MAX_PENDING_MSG=-1")

start_time = time.time()
for config in configs:
    config = get_default_config(config)
    print("Config: " + json.dumps(config))

    pshell.update_env(get_env_vars(config))
    # pshell.run("export LCI_SERVER_NUM_PKTS=655360")
    # pshell.run("export LCI_PACKET_SIZE=65536")

    scenario = "rs"
    if "scenario" in config:
        scenario = config["scenario"]
    scenarios_path = get_platform_config("scenarios_path", config)[scenario].replace("%root%", root_path)
    pshell.run(f"cd {scenarios_path}")

    cmd = (get_platform_config("get_srun_args", config) +
           get_platform_config("get_numactl_args", config) +
           get_args(config)
           # + ["--hpx:ini=hpx.max_busy_loop_count=1"]
           )
    pshell.run(cmd)
end_time = time.time()
print("Executed {} configs. Total time is {}s.".format(len(configs), end_time - start_time))