'''
import subprocess_tee
import logging

def execute(cmd, cmd_name, cwd=None, stdout=None):
    """
    Execute a command.

    Args:
        cmd (str): Command to execute.
        cmd_name (str): Name of the command.
        cwd (_type_, optional): Working directory to execute the command in. Defaults to None.
        stdout (_type_, optional): Output file. Defaults to None.

    Returns:
        _type_: _description_
    """
    try:
        logging.debug(f"Running command: {cmd}")
        if stdout:
            logging.info(f"[assembly-scan] {cmd_name} > {stdout}")
            with open(stdout, "w") as out:
                subprocess_tee.run(cmd, shell=True, cwd=cwd, stdout=out, stderr=subprocess.PIPE, check=True)
        else:
            logging.info(f"[assembly-scan] {cmd_name}")
            result = subprocess_tee.run(cmd, shell=True, cwd=cwd, check=True, text=True)
            return [result.stdout, result.stderr]
    except subprocess_tee.CalledProcessError as e:
        logging.error(f"Error running {cmd_name}: {e}")
        return False
    return True
'''
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from subprocess import PIPE, CalledProcessError, CompletedProcess, Popen


def execute(
    args,
    cmd_name,
    *,
    stdout_handler,
    stderr_handler,
    check=True,
    text=True,
    stdout=PIPE,
    stderr=PIPE,
    **kwargs,
):
    """Mimic subprocess.run, while processing the command output in real time."""
    with (
        Popen(args, text=text, stdout=stdout, stderr=stderr, **kwargs) as process,
        ThreadPoolExecutor(2) as pool,  # two threads to handle the (live) streams separately
    ):
        exhaust = partial(deque, maxlen=0)  # collections recipe: exhaust an iterable at C-speed
        exhaust_async = partial(pool.submit, exhaust)  # exhaust non-blocking in a background thread
        exhaust_async(stdout_handler(line[:-1]) for line in process.stdout)
        exhaust_async(stderr_handler(line[:-1]) for line in process.stderr)
    retcode = process.poll()  # block until both iterables are exhausted (process finished)
    if check and retcode:
        raise CalledProcessError(retcode, process.args)
    #return CompletedProcess(process.args, retcode)
    return [1, 2]
