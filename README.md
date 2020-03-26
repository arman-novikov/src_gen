Если папка или файлы уже существуют сработает защита
(чтобы случайно не потерять свои исходники).

для прогеров:
WINDOWS:
	в случае проблем с импортом идём в python3X\Lib\site-packages\PyQt5\Qt\plugins;
	копируем папку platforms в директорию с экзешником питона

	сборка:
		pyinstaller --noconsole --onefile --icon=icon.png main.py