#!/bin/bash

parallel_dir="outputs/parallel"
serial_dir="outputs/serial"

# Flag to track if all files match
all_match=true

# Verify Outputs for E
for parallel_file in "$parallel_dir"/fdtd_parallel_E_*.txt; do
    filename=$(basename "$parallel_file")

    timestep="${filename#fdtd_parallel_E_}"
    timestep="${timestep%.txt}"

    serial_file="$serial_dir/fdtd_serial_E_${timestep}.txt"

    if [[ ! -f "$serial_file" ]]; then
        echo "Missing file: $serial_file"
        all_match=false
        continue
    fi

    # Compare the files
    if ! diff -q "$parallel_file" "$serial_file" > /dev/null; then
        echo "Difference found at timestep $timestep"
        all_match=false
    fi
done

# Verify Outputs for H
for parallel_file in "$parallel_dir"/fdtd_parallel_H_*.txt; do
    filename=$(basename "$parallel_file")

    timestep="${filename#fdtd_parallel_H_}"
    timestep="${timestep%.txt}"

    serial_file="$serial_dir/fdtd_serial_H_${timestep}.txt"

    if [[ ! -f "$serial_file" ]]; then
        echo "Missing file: $serial_file"
        all_match=false
        continue
    fi

    # Compare the files
    if ! diff -q "$parallel_file" "$serial_file" > /dev/null; then
        echo "Difference found at timestep $timestep"
        all_match=false
    fi
done

# Print summary result
if $all_match; then
    echo  "SUCCESS: Serial and Parallel Match! :) "
    exit 0
else
    echo "FAIL: Some timestamps differ :("
    exit 1
fi
