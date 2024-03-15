#!/bin/bash


for file in ./youtube8m/*/*/*.wav; do
    echo $file
    mv -n $file ./y8m_audios/
done

echo "Total complete"

