cd ..\build\PyPI
py -m pip install --upgrade twine
py -m twine upload -r testpypi -u __token__ -p pypi-AgENdGVzdC5weXBpLm9yZwIkZmZhNmViNDYtOGQwYy00ZDJkLTlmY2UtMmQ4NTBmZDllMGQyAAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiCb2901t3Sx0CX74EWKb9ZJLwEIL0BKwG9GW1rnMloipA dist/*
cd ..\..\tools
pause