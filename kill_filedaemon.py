import os
import signal
import sys

def kill_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Process with PID {pid} killed.")
    except ProcessLookupError:
        print(f"No process found with PID {pid}.")

def get_filedaemon_pid():
    data = ""
    try:
        with open("filedaemon_pid.txt") as file:
            data = file.readline()
    except:
        print("Could not find filedaemon pid file")
        sys.exit(0)
    if not data:
        print("Could not read data from filedaemon pid file")
        sys.exit(0)
    return int(data)

# You can replace the value in process_pid with the actual PID of the process you want to kill
process_pid = get_filedaemon_pid()
kill_process(process_pid)