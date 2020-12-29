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

def renameItem(section, oldKey, newKey, subsection = None):
	conf = getConfig()
	if subsection:
		conf[section][subsection].rename(oldKey, newKey)
	else:
		conf[section].rename(oldKey, newKey)
	conf.write()

def getSubsectionsFromSection(section, exc = None):
	conf = getConfig()
	sbList = []
	for sb in conf[section].keys():
		if isinstance(conf[section][sb], configobj.Section):
			if not sb == exc:
				sbList.append(sb)
	return sbList

def modifyValue(section, key, value, subsection = None):
	conf = getConfig()
	if subsection:
		conf[section][subsection][key] = value
	else:
		conf[section][key] = value
	conf.write()
	return True

def delItem(section, key, subsection = None):
	conf = getConfig()
	if subsection:
		del(conf[section][subsection][key])
	else:
		del(conf[section][key])
	conf.write()

def getSubsectionsOrKeysList(section):
	conf = getConfig()
	theList = []
	for item in conf[section].items():
		if isinstance(item, configobj.Section):
			theList.append(item)
		elif isinstance(item, tuple):
			theList.append(item[0])
	return theList
