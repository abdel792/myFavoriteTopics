# coding:utf-8

import os
import shutil
import globalVars
import sys
if sys.version_info.major == 2:
	import io
	open = io.open

CONFIG_FILE_NAME = "myFavoriteTopics.ini"

def onInstall():
	if not os.path.exists(os.path.join(globalVars.appArgs.configPath, CONFIG_FILE_NAME)):
		shutil.move(os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME), os.path.join(globalVars.appArgs.configPath, CONFIG_FILE_NAME))
	else:
		f = open (os.path.join(globalVars.appArgs.configPath, CONFIG_FILE_NAME), "a+", encoding = "utf-8")
		f.seek(0)
		content = f.read()
		if "[myNotes]" not in content:
			f.seek(0, 2)
			f.write ("[myNotes]")
		f.close()
		