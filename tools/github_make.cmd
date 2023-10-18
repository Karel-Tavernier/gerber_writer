cd ..\build
rmdir github\docs /s /q
xcopy docs\html\*.* github\docs /e /v /i
copy ..\doc\.nojekyll github\docs /v
copy ..\doc\LICENSE github /v
copy ..\src\PyPI\README.rst github /v
rmdir github\examples /s /q
xcopy ..\examples\*.* github\examples /e /v /i
rmdir github\src\gerber_writer /s /q
xcopy ..\src\gerber_writer\*.py github\src\gerber_writer /e /v /i
cd ..\tools
pause
