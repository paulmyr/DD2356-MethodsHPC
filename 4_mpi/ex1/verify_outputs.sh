#!/bin/bash

parallel_dir="outputs/parallel"
serial_dir="outputs/serial"

# Flag to track if all files match
all_match=true

# Loop over all parallel output files
for parallel_file in "$parallel_dir"/wave_output_parallel_*.txt; do
    filename=$(basename "$parallel_file")

    timestep="${filename#wave_output_parallel_}"
    timestep="${timestep%.txt}"

    serial_file="$serial_dir/wave_output_serial_${timestep}.txt"

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
