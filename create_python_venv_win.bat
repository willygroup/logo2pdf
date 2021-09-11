python -m venv .win_env & .win_env/Script/activate & pip install -r requirements.txt

@echo rem  cp .\.win_env\Lib\site-packages\shiboken2\shiboken2.abi3.dll .\.win_env\Lib\site-packages\PySide2\ 
@echo rem mkdir .\dist\main\barcode\fonts\ 
@echo rem cp .\various\DejaVuSansMono.ttf .\dist\main\barcode\fonts\ 
@echo rem cp -r .\files\ .\dist\main\ 
