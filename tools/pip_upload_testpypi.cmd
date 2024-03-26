cd ..\pip
py -m pip install --upgrade twine
py -m twine upload --repository testpypi dist/*
cd ..\tools
pause