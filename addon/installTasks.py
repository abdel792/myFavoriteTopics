# coding:utf-8

import os
import shutil
import globalVars

CONFIG_FILE_NAME = "myFavoriteTopics.ini"

def onInstall():
	shutil.move(os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME), os.path.join(globalVars.appArgs.configPath, CONFIG_FILE_NAME))
