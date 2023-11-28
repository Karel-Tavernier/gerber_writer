#! /bin/bash
echo $1
while true ; do
	if [[ $PWD = "/" ]]; then
		echo "we could not find the project directory gerber_writer_project"
		break 
	fi
#    echo "base=$(basename $PWD) on path $PWD"
    if [[ "$(basename $PWD)" =~ $1 ]]; then
        break
    fi
    cd ..
done
pwd
