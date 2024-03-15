#!/bin/bash

total_dirs=0

# Iterate over all MP4 files in the folder
for dir in ./youtube8m/*/*; do
    echo $dir
    cp -n $dir/*.wav ./y8m_audios/
    total_dirs=`expr $total_dirs + 1`
done

echo "Total dirs: $total_dirs"

