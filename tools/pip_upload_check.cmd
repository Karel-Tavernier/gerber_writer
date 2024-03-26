cd ..\pip
pip -m pip --install --upgrade pip
py -m pip install --upgrade twine
twine check dist/*
cd ..\tools
pause