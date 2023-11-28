#! /bin/bash
prev=.
while [[ $PWD != "$prev" ]] ; do
    echo $PWD
    find "$PWD" -maxdepth 1 "$@"
    prev=$PWD
    cd ..
done
