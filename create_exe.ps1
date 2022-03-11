New-Item -Path ".\" -Name "dist\" -ItemType "directory" -Force
Remove-Item '.\dist\' -Recurse -ErrorAction Ignore && pyinstaller.exe -F -w --onedir --noconsole  .\main.py 