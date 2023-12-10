import os
import sys
import shutil
import copy
import glob
import json
from platform_config_base import *
import pshell

def rm(dir):
    try:
        shutil.rmtree(dir)
        print(f"Directory {dir} has been deleted successfully.")
    except OSError as e:
        print(f"Error: {dir} : {e.strerror}")

def mv(source, destination):
    try:
        source_files = glob.glob(source)
        for file in source_files:
            destination_filename = destination
            if os.path.isdir(destination_filename):
                destination_filename = os.path.join(destination_filename, os.path.basename(file))
            shutil.move(file, destination_filename)
            print(f"Moved '{file}' to '{destination_filename}'")
    except FileNotFoundError:
        print(f"Error: '{source}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied while moving '{source}'.")
    except shutil.Error as e:
        print(f"Error: Failed to move '{source}' to '{destination}': {e}")

def mkdir_s(dir):
    if os.path.exists(dir):
        prompt = "{} directory exists. Are you sure to remove it | continue with it | or abort? [r|c|A]".format(dir)
        print(prompt)
        x = input()
        if x == "r":
            print("Remove {}".format(dir))
            rm(dir)
        elif x == "c":
            print("Continue with previous work")
        else:
            print("Abort")
            sys.exit(1)

    if not os.path.exists(dir):
        os.mkdir(dir)

def getenv_or(key, default):
    if key in os.environ:
        return os.environ[key]
    else:
        return default

def get_current_script_path():
    if "CURRENT_SCRIPT_PATH" in os.environ:
        return os.environ["CURRENT_SCRIPT_PATH"]
    else:
        return os.path.realpath(sys.argv[0])

def get_module():
    init_file = get_platform_config("module_init_file")
    if init_file is None:
        module_home = os.environ["MODULESHOME"]
        module_init_file_path = os.path.join(module_home, "init", "*.py")
        init_files = glob.glob(module_init_file_path)
        if len(init_files) != 1:
            print("Cannot find init file {}".format(init_files))
        init_file = init_files[0]
    print("Load init file {}".format(init_file))
    dir_name = os.path.dirname(init_file)
    file_name = os.path.basename(init_file)
    name = os.path.splitext(file_name)[0]
    if dir_name not in sys.path:
        sys.path.insert(0, dir_name)
    module = getattr(__import__(name, fromlist=["module"]), "module")
    return module

def module_list():
    os.system("module list")

def spack_env_activate(env):
    _, ret_stderr = pshell.run("spack env activate {}".format(env), to_print=False)
    if ret_stderr:
        for line in ret_stderr.splitlines():
            if "setup-env.sh" in line:
                pshell.run(line.strip())
                _, ret_stderr = pshell.run("spack env activate {}".format(env))
                break
    if ret_stderr:
        print(ret_stderr)
    assert not ret_stderr
    # ret_stdout, _ = pshell.run("spack env activate --sh {}".format(env), to_print=False)
    # if ret_stdout:
    #     pshell.run(ret_stdout.replace("\n", " ").strip()[:-1], to_print=False)

def submit_pbs_job(job_file, tag, nnodes, config, time, name, partition, extra_args):
    if name is None:
        name = config["name"]
    pbs_args = [f"-A {get_platform_config('account', config, partition)}",
                "-k doe",
                f"-l walltime={time}",
                f"-l select={nnodes}",
                f"-N {tag}-{name}",
                f"-q {get_platform_config('partition', config, partition)}"
                ]
    if get_platform_config("additional_sbatch_args", config, extra_args):
        pbs_args += get_platform_config("additional_sbatch_args", config, extra_args)
    pshell.run(["qsub"] + pbs_args + [job_file])

def submit_slurm_job(job_file, tag, nnodes, config, time, name, partition, extra_args):
    if name is None:
        name = config["name"]
    ntasks_per_node = 1
    if "ntasks_per_node" in config:
        ntasks_per_node = config["ntasks_per_node"]
    job_name="n{}-t{}-{}".format(nnodes, ntasks_per_node, name)
    output_filename = "./run/slurm_output.{}.%x.j%j.out".format(tag)
    sbatch_args = ["--export=ALL",
                   f"--nodes={nnodes}",
                   f"--job-name={job_name}",
                   f"--output={output_filename}",
                   f"--error={output_filename}",
                   f"--time={time}",
                   f"--ntasks-per-node={ntasks_per_node}",
                   f"--cpus-per-task={int(get_platform_config('cpus_per_node', config) / ntasks_per_node)}",
                   ]
    gpus_per_node = int(get_platform_config("gpus_per_node", config) / ntasks_per_node)
    if gpus_per_node:
        sbatch_args.append(f"--gpus-per-task={gpus_per_node}")
    if get_platform_config("account", config):
        sbatch_args.append("--account={}".format(get_platform_config("account", config)))
    if not partition:
        partition = get_platform_config("partition", config)
    if partition:
        sbatch_args.append("--partition={} ".format(partition))
    if get_platform_config("qos", config):
        sbatch_args.append("--qos={} ".format(get_platform_config("qos", config)))
    sbatch_args += get_platform_config("additional_sbatch_args", config, [])
    if extra_args:
        sbatch_args += extra_args

    current_path = get_current_script_path()
    command = f"sbatch {' '.join(sbatch_args)} {job_file} '{current_path}' '{json.dumps(config)}'"
    pshell.run(command)

def submit_job(job_file, tag, nnodes, config, time="00:05:00", name=None, partition=None, extra_args=None):
    scheduler = get_platform_config("scheduler", config, "slurm")
    if scheduler == "slurm":
        submit_slurm_job(job_file, tag, nnodes, config, time, name, partition, extra_args)
    elif scheduler == "pbs":
        submit_pbs_job(job_file, tag, nnodes, config, time, name, partition, extra_args)

if __name__ == "__main__":
    spack_env_activate("hpx-lci")