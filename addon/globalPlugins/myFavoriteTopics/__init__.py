# coding:utf-8

# globalPlugins/myFavoriteTopics/__init__.py.

# Copyright 2017-2019 Abdelkrim Bensaïd and other contributors, released under gPL.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import globalPluginHandler
from . import myConfig
import wx
import gui
from . import dialogs

# Importing the SCRCAT_TOOLS category from the globalCommands module.
from globalCommands import SCRCAT_TOOLS

# For translation.
import addonHandler
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = SCRCAT_TOOLS
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self.createSubMenu()

	def createSubMenu(self):
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		# Translators: Item in the tools menu for the Addon myFavoriteTopics.
		self.myFavoriteTopics = self.toolsMenu.Append(wx.ID_ANY, _("&My favorite topics..."),
		"")
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onMyFavoriteTopicsDialog, self.myFavoriteTopics)

	def terminate(self):
		try:
			self.toolsMenu.RemoveItem(self.myFavoriteTopics)
		except wx.PyDeadObjectError:
			pass

	def onMyFavoriteTopicsDialog(self, evt):
		if gui.isInMessageBox:
			return
		gui.mainFrame.prePopup()
		d = dialogs.MyFavoriteTopicsDialog(parent = gui.mainFrame)
		d.Show(True)
		gui.mainFrame.postPopup()

	def script_myPreferredSites(self, gesture):
		wx.CallAfter (self.selectItemInList, section="mySites")

	def script_myApps(self, gesture):
		wx.CallAfter (self.selectItemInList, section="myApps")

	def script_myNews(self, gesture):
		wx.CallAfter (self.selectItemInList, section="myNews")

	def script_myContacts(self, gesture):
		wx.CallAfter (self.selectItemInList, section="myContacts")
	

	def script_activateMyFavoriteTopicsDialog(self, gesture):
		wx.CallAfter(self.onMyFavoriteTopicsDialog, gui.mainFrame)

	def selectItemInList (self, section):
		if gui.isInMessageBox:
			return
		gui.mainFrame.prePopup ()
		d = dialogs.MyTopicsDialog(parent = gui.mainFrame, section=section)
		d.Show(True)
		gui.mainFrame.postPopup ()

	# Translators: Message presented in input help mode.
	script_activateMyFavoriteTopicsDialog.__doc__=_("Allows you to display the dialog box to select uour favorite topics.")
	script_myPreferredSites.__doc__=_("Allows you to display a dialog box to select your favorite websites")
	script_myApps.__doc__=_("Allows you to display a dialog box to select your favorite applications or directories")
	script_myContacts.__doc__=_("Allows you to display a dialog box to select your favorite contacts")
	script_myNews.__doc__=_("Allows you to display a dialog box to select your favorite journal websites")
