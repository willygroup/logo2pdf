New-Item -Path ".\" -Name "dist\" -ItemType "directory" -Force
Remove-Item '.\dist\' -Recurse -ErrorAction Ignore && pyinstaller.exe -F -w --onedir --noconsole  .\main.py && copy .\files\ .\dist\main\ -Recurse && New-Item -Path ".\dist\main\" -Name "barcode\fonts\" -ItemType "directory" && copy .\various\DejaVuSansMono.ttf .\dist\main\barcode\fonts\

#This won't work && Move-Item -Path ".\dist\main\main.exe" -Destination ".\dist\main\csv2lbl.exe"
 