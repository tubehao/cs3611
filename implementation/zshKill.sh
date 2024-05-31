#!/bin/zsh

# Find all Python processes that are running Node.py
pids=$(ps aux | grep "python.*Node.py" | grep -v grep | awk '{print $2}')

# Check if there are any PIDs to kill
if [ -z "$pids" ]; then
    echo "No Node.py processes found."
else
    # Kill each PID
    for pid in ${(ps:\n:)pids}; do
        kill -9 $pid
        echo "Killed process with PID $pid"
    done
fi

echo "Done killing subprocesses."