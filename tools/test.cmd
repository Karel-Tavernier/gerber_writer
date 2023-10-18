set PYTHONPATH=..\src;%PATH%
py ..\tests\gerber_writer_doctest.py
cd ..\src
coverage run -m --timid unittest gerber_writer\writer_test.py
coverage report -m
del .coverage
cd ..\tests
py gerber_writer_doctest.py
pytest
cd ..\tools
pyflakes ..\src\gerber_writer\writer.py
pyflakes ..\src\gerber_writer\padmasters.py
pause
