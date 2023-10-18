rmdir ..\build\PyPI /s /q
mkdir ..\build\PyPI
xcopy ..\src\gerber_writer\*.* ..\build\PyPI\src\gerber_writer /v /i
copy  ..\src\PyPi\pyproject.toml ..\build\PyPI\ /v /y
copy ..\src\PyPI\README.rst ..\build\PyPI\ /v
copy ..\doc\LICENSE ..\build\PyPI\ /v
del ..\build\PyPI\dist\*.* /q
cd ..\build\PyPI
py -m pip install --upgrade pip
py -m pip install --upgrade build
py -m build
py -m pip install --upgrade twine
twine check dist/*
cd ..\..\tools
pause