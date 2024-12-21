#!/bin/bash

# Variables
dd="/path/to/destination_directory"  # Replace with your destination path
now=$(date '+%Y-%m-%d %H:%M:%S')     # Current timestamp for logging
src_dir="/home/wrf/uems/runs/southern_africa/emsprd/grads/d02htm"
grads_dir="/home/wrf/uems/runs/southern_africa/emsprd/grads"

# Check if source directory exists
if [ -d "$src_dir" ]; then
    echo "Source directory exists: $src_dir"

    # Change to the grads directory
    cd "$grads_dir" || {
        echo "Failed to change directory to $grads_dir. Exiting."
        exit 1
    }

    # Copy the source directory to the destination
    echo "Copying $src_dir to $dd..."
    cp -r "$src_dir" "$dd" && echo "Finished copying $src_dir to $dd at $now" || {
        echo "Error: Failed to copy $src_dir to $dd"
        exit 1
    }
else
    echo "Source directory does not exist: $src_dir"
fi
