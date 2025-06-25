python -m venv .win_env && &".\.win_env\Scripts\activate" && python -m pip install --upgrade pip && pip install wheel && pip install -r requirements.txt && pip install pyinstaller

Write-Host "Done!"
Write-Host "type: 'python main.py' to launch the application"
