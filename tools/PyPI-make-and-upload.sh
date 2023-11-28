#!/bin/bash
# 231025 adf linux version of make. this script will upload the project to testPYPI
# 231025 adf run as "./PyPI-make-and-upload.sh"
# 		-- do not use "sh PyPI-make-and-upload.sh" (sh does not understand "select" cmd)
pwd

# change to project directory. -- return to current dir after execution of this script.
while true ; do
	if [[ $PWD = "/" ]]; then
		echo "we could not find the project directory gerber_writer_project"
		exit 
	fi
#    echo "base=$(basename $PWD) on path $PWD"
    if [[ "$(basename $PWD)" =~ "gerber_writer_project" ]]; then
        break
    fi
    cd ..
done

if ! test -d src/PyPI; then
  echo "this does not seem to be the dir with src and PyPI. try again."
fi
read -p "=> now removing previous dist.                         if you prefer to quit press CTRL-C" answer
rm -rf dist/*
read -p "=> dist removed. now removing previous __pycache__     if you prefer to quit press CTRL-C" answer
find . -iname '__pycache__' -type d -exec rm -r {} \;
read -p "=> __pycache__ files removed.                          if you want to quit press CTRL-C" answer
# mkdir -p build/PyPI/$proj
# cp -r $proj/* build/PyPI/$proj/
find . -iname '.pytest_*' -exec rm -r {} \;
read -p "=> starting build                                      if you want to quit press CTRL-C" answer
python3 -m build
read -p "=> you can check now the dist directory                if you want to quit press CTRL-C" answer
#echo "user should be __token__, get token from bitwarden"
echo "do you have a token?"
select ynn in Yes "No, I will go with your token" No
do
	case $ynn in
		Yes )
			python3 -m pip install --upgrade pip
			python3 -m pip install --upgrade twine
			python3 -m twine upload --repository testpypi -u __token__ dist/* --verbose
			break;;
		"No, I will go with your token"  )
			python3 -m pip install --upgrade pip
			python3 -m pip install --upgrade twine
			python3 -m twine upload  -r testpypi -u __token__ -p pypi-AgENdGVzdC5weXBpLm9yZwIkYTg4Yzk2YTItOGZkNC00NTdlLThhNjItMTdhZmI4MWQxNjgwAAIqWzMsImEwM2QxZDM0LWIyZmYtNDA0ZC05ZTI3LWU1OTY2MDQxZTFhYSJdAAAGIIKJCl5VbDDkS4QOfCjetRWtipxrheFI1v28DMekYoPG dist/* --verbose
            exit;;
		No  )
            echo "get one on PyPI website in your account! or retry with option 2"
            exit;;
	esac
done

