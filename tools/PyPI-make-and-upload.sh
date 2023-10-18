#!/bin/bash
#set -x
#trap read debug
cd /home/alaindef/projects/pycharm-projects-py3/gerber_writer/
if ! test -d src/PyPI; then
  echo "this does not seem to be the dir with src and PyPI. try again."
fi
# echo "=> we are in project $proj"
# read -p "=> removing previous build                             if you prefer to quit press CTRL-C"
# rm -rf build
# read -p "=> build removed. now removing previous dist.          if you prefer to quit press CTRL-C"
read -p "=> now removing previous dist.                         if you prefer to quit press CTRL-C"
rm -rf dist/*
read -p "=> dist removed. now removing previous __pycache__     if you prefer to quit press CTRL-C"
find . -iname '__pycache__' -type d -exec rm -r {} \;
read -p "=> __pycache__ files removed.                          if you want to quit press CTRL-C"
# mkdir -p build/PyPI/$proj
# cp -r $proj/* build/PyPI/$proj/
find . -iname '.pytest_*' -exec rm -r {} \;
# echo "=> current dir $(pwd)"
read -p "=> starting build                                      if you want to quit press CTRL-C"
python3 -m build
read -p "=> you can check now the dist directory                if you want to quit press CTRL-C"
#echo "user should be __token__, get token from bitwarden"
echo -e "do you have a token?"
select ynn in "Yes" "No, I will go with your token" "No"; do
	case $ynn in
		'Yes' )
		  python3 -m pip install --upgrade pip
      python3 -m pip install --upgrade twine
			python3 -m twine upload --repository testpypi -u __token__ dist/* --verbose
			break;;
		'No, I will go with your token'  )
		  python3 -m pip install --upgrade pip
      python3 -m pip install --upgrade twine
			python3 -m twine upload  -r testpypi -u __token__ -p pypi-AgENdGVzdC5weXBpLm9yZwIkYTg4Yzk2YTItOGZkNC00NTdlLThhNjItMTdhZmI4MWQxNjgwAAIqWzMsImEwM2QxZDM0LWIyZmYtNDA0ZC05ZTI3LWU1OTY2MDQxZTFhYSJdAAAGIIKJCl5VbDDkS4QOfCjetRWtipxrheFI1v28DMekYoPG dist/* --verbose
            exit;;
		'No'  )
            echo "get one on PyPI website in your account! or retry with option 2"
            exit;;
	esac
done
# python3 -m pip install --index-url https://test.pypi.org/simple/

