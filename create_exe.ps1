Remove-Item '.\dist\' -Recurse -ErrorAction Ignore && pyinstaller.exe --onedir  .\main.py 
