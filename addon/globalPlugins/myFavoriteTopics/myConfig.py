# coding:utf-8

# globalPlugins/myFavoriteTopics/myConfig.py.

# Copyright 2017-2019 Abdelkrim Bensaïd and other contributors, released under gPL.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import configobj
import globalVars

CONFIG_FILE_NAME = "myFavoriteTopics.ini"
CONFIG_FILE_PATH = os.path.join(globalVars.appArgs.configPath, CONFIG_FILE_NAME)

def getConfig():
	_config = configobj.ConfigObj(CONFIG_FILE_PATH, encoding="UTF-8")
	return _config

def renameKey(section, oldKey, newKey):
	conf = getConfig()
	conf[section].rename(oldKey, newKey)
	conf.write()

def getKeyFromValue(section, value):
	conf = getConfig()
	key = conf[section].keys()[conf[section].values().index(value)]
	return key

def modifyValue(section, key, value):
	conf = getConfig()
	conf[section][key] = value
	conf.write()
	return True

def delItem(section, key):
	conf = getConfig()
	del(conf[section][key])
	conf.write()
