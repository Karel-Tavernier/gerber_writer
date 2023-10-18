cd ..\build\PyPI
py -m pip install --upgrade pip
py -m pip install --upgrade twine
py -m twine upload -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGEyOTI4YThiLWY1NmMtNGZlOC05YTM5LWJmYWQ5YjI4YjcwZAACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgbMqvuCg_vl4ieeo7_Wr6U1Ntolnb5LrVhpOv1GF5HF0 dist/*
cd ..\..\tools
pause