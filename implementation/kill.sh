#!/bin/bash

# Find all Python processes that are running Node.py
pids=$(ps aux | grep 'python Node.py' | grep -v grep | awk '{print $2}')

# Check if there are any PIDs to kill
if [ -z "$pids" ]; then
  echo "No Node.py processes found."
else
  # Kill each PID
  for pid in $pids; do
    kill -9 $pid
    echo "Killed process with PID $pid"
  done
fi

echo "Done killing subprocesses."

#pids=$(netstat -anp 2>/dev/null | awk '$4 ~ /127\.0\.0\.1:600[0-9][0-9]/ && /python/ {print $7}' | awk -F'/' '{print $1}' | sort -u)
#
#if [ -z "$pids" ]; then
#    echo "No Python processes found on ports > 60000"
#    exit 0
#fi
#
#for pid in $pids; do
#    echo "Killing process $pid"
#    kill -9 $pid
#done
#
#echo "Done killing ports holders."

