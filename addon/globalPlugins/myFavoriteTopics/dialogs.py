# coding:utf-8

# globalPlugins/myFavoriteTopics/dialogs.py.

# Copyright 2017-2019 Abdelkrim Bensaïd and other contributors, released under gPL.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import myConfig
import globalVars
import gui
import os
import webbrowser
import subprocess
from logHandler import log

# For translation.
import addonHandler
addonHandler.initTranslation()

class MyFavoriteTopicsDialog(wx.Dialog):
	_instance = None

	def __new__(cls, *args, **kwargs):
		if MyFavoriteTopicsDialog._instance is None:
			return super(MyFavoriteTopicsDialog, cls).__new__(cls, *args, **kwargs)
		return MyFavoriteTopicsDialog._instance

	def __init__(self, parent):
		if MyFavoriteTopicsDialog._instance is not None:
			return
		MyFavoriteTopicsDialog._instance = self
		# Translators: The title of the favorite topics dialog.
		super(MyFavoriteTopicsDialog, self).__init__(parent, title = _("My favorite topics"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)

		# Translators: The label of a button to display the list of the favorite websites.
		item = self.websitesListButton = wx.Button(self, label = _("Display my favorite &websites"))
		item.Bind(wx.EVT_BUTTON, self.onDisplayWebsites)
		sizer.Add(item)

		# Translators: The label of a button to display the list of the favorite applications or directories.
		item = self.appsListButton = wx.Button(self, label = _("Display my favorite &applications"))
		item.Bind(wx.EVT_BUTTON, self.onDisplayApps)
		sizer.Add(item)

		# Translators: The label of a button to display the list of the favorite contacts.
		item = self.contactsListButton = wx.Button(self, label = _("Display my favorite &contacts"))
		item.Bind(wx.EVT_BUTTON, self.onDisplayContacts)
		sizer.Add(item)

		# Translators: The label of a button to display the list of the favorite journal websites.
		item = self.newsListButton = wx.Button(self, label = _("Display my favorite &journal websites"))
		item.Bind(wx.EVT_BUTTON, self.onDisplayNews)
		sizer.Add(item)

		mainSizer.Add(sizer)
		# Translators: The label of a button to close the dialog.
		item = wx.Button(self, wx.ID_CLOSE, label = _("&Close"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(item)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE

		if globalVars.appArgs.secure:
			for item in self.websitesListButton, self.appsListButton, self.contactsListButton, self.newsListButton:
				item.Disable()
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def __del__(self):
		MyFavoriteTopicsDialog._instance = None

	def onDisplayWebsites(self, evt):
		d = MyTopicsDialog(parent = self, section = "mySites")
		d.Show()

	def onDisplayApps(self, evt):
		d = MyTopicsDialog(parent = self, section = "myApps")
		d.Show()

	def onDisplayContacts(self, evt):
		d = MyTopicsDialog(parent = self, section = "myContacts")
		d.Show()

	def onDisplayNews(self, evt):
		d = MyTopicsDialog(parent = self, section = "myNews")
		d.Show()

	def onClose(self, evt):
		self.Destroy()

class MyTopicsDialog(wx.Dialog):

	_instance = None
	def __new__(cls, *args, **kwargs):
		if MyTopicsDialog._instance is None:
			return super(MyTopicsDialog, cls).__new__(cls, *args, **kwargs)
		return MyTopicsDialog._instance

	def __init__(self, parent, section):
		if MyTopicsDialog._instance is not None:
			return
		MyTopicsDialog._instance = self
		self.section = section
		if section == "mySites":
			topics = [_("favorite websites"), _("Websites")]
		elif section == "myApps":
			topics = [_("favorite applications or directories"), _("Applications or directories")]
		elif section == "myContacts":
			topics = [_("favorite contacts"), _("Contacts")]
		elif section == "myNews":
			topics = [_("favorite journal websites"), _("journal websites")]
		# Translators: The title of the topics dialog.
		super(MyTopicsDialog, self).__init__(parent, title = _("My {theTopics}").format(theTopics = topics[0]))
		self.itemsList = []
		self.itemsList.extend(myConfig.getConfig()[section].keys())
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of the items list.
		sizer.Add(wx.StaticText(self, label = topics[1]))
		item = self.topicsList = wx.ListBox(self, 
		choices = self.itemsList,
		style = wx.LB_SORT)
		sizer.Add(item)
		mainSizer.Add(sizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a button to open an element in the topics list.
		item = self.openButton = wx.Button(self, label = _("&Open"))
		item.Bind(wx.EVT_BUTTON, self.onOpen)
		item.SetDefault()
		sizer.Add(item)
		# Translators: The label of a button to create a new element in the topics list.
		item = self.addButton = wx.Button(self, label = _("&Add"))
		item.Bind(wx.EVT_BUTTON, self.onNew)
		sizer.Add(item)
		# Translators: The label of a button to rename an element in the topics list.
		item = self.renameKeyButton = wx.Button(self, label = _("&Rename the key"))
		item.Bind(wx.EVT_BUTTON, self.onRenameKey)
		sizer.Add(item)
		# Translators: The label of a button to modify the value of an item in the topics list.
		item = self.modifyValueButton = wx.Button(self, label = _("&Modify value"))
		item.Bind(wx.EVT_BUTTON, self.onModifyValue)
		sizer.Add(item)
		# Translators: The label of a button to remove an item in the topics list.
		item = self.deleteButton = wx.Button(self, label = _("&Delete"))
		item.Bind(wx.EVT_BUTTON, self.onDelete)
		sizer.Add(item)
		mainSizer.Add(sizer)
		# Translators: The label of a button to close the dialog.
		item = wx.Button(self, wx.ID_CLOSE, label = _("&Close"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(item)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE
		self.onDisableOrEnableButtons()
		if self.topicsList.GetCount() > 0:
			self.topicsList.Selection = 0

		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.topicsList.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def __del__(self):
		MyTopicsDialog._instance = None

	def onDisableOrEnableButtons(self):
		if globalVars.appArgs.secure:
			for item in self.openButton, self.addButton, self.renameKeyButton, self.modifyValueButton, self.deleteButton:
				item.Disable()
		else:
			for item in self.openButton, self.renameKeyButton, self.modifyValueButton, self.deleteButton:
				if len(myConfig.getConfig()[self.section].keys()) == 0:
					item.Disable()
				else:
					item.Enable()

	def onNew(self, evt):
		NewElementDialog(self).Show()
		evt.Skip()

	def onDelete(self, evt):
		if self.topicsList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the topics list.
			gui.messageBox(
			message = _("No selection found ! Please select an item in the list"),
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.topicsList.Selection
		if gui.messageBox(
			# Translators: The confirmation prompt displayed when the user requests to delete an element in the topics list.
			message = _("Are you sure you want to delete {theKey}?").format(theKey = self.topicsList.GetString(index)),
			# Translators: The title of the confirmation dialog for deletion of an element in the topics list.
			caption = _("Confirm Deletion"),
			style = wx.YES | wx.NO | wx.ICON_QUESTION, parent = self
		) == wx.NO:
			return
		key = self.topicsList.GetString(index)
		try:
			myConfig.delItem(self.section, key)
		except:
			log.debugWarning("", exc_info = True)
			# Translators: An error displayed when deleting an element fails.
			gui.messageBox(message = _("Error deleting element."),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		self.onDisableOrEnableButtons()
		del self.itemsList[self.itemsList.index(key)]
		self.topicsList.Delete(index)
		self.topicsList.Selection = index - 1 if index == self.topicsList.GetCount() else index or 0
		self.topicsList.SetFocus()

	def onRenameKey(self, evt):
		if self.topicsList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the topics list.
			gui.messageBox(
			message = _("No selection found ! Please select an item in the list"),
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.topicsList.Selection
		oldName = self.topicsList.GetString(index)
		# Translators: The label of a field to enter a new name for the key.
		with wx.TextEntryDialog(self, _("New name:"),
				# Translators: The title of the dialog to rename the key.
				_("Rename the key"), defaultValue = oldName) as d:
			if d.ShowModal() == wx.ID_CANCEL:
				return
			newName = d.Value
		if newName in myConfig.getConfig()[self.section].keys():
			# Translators: An error displayed when the key already exists.
			gui.messageBox(message = _("This name already exists. Please choose a different name"), caption = _("Error"), style = wx.OK|wx.ICON_ERROR, parent = self)
		try:
			myConfig.renameKey(self.section, oldName, newName)
		except (KeyError, ValueError):
			# Translators: An error displayed when renaming a key fails.
			gui.messageBox(message = _("Can not rename this key."),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		except:
			log.debugWarning("", exc_info = True)
				# Translators: An error displayed when renaming a key fails.
			gui.messageBox(message = _("Error renaming key."),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		self.itemsList[self.itemsList.index(oldName)] = newName
		self.topicsList.Set(self.itemsList)
		self.topicsList.SetSelection(self.topicsList.FindString(newName))
		self.topicsList.SetFocus()

	def onModifyValue(self, evt):
		if self.topicsList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the topics list.
			gui.messageBox(
			message = _("No selection found ! Please select an item in the list"),
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.topicsList.Selection
		theKey = self.topicsList.GetString(index)
		# Translators: The label of a field to enter a new value for the key.
		with wx.TextEntryDialog(self, _("New value:"),
				# Translators: The title of the dialog to modify the value.
				_("Modify the value"), defaultValue = myConfig.getConfig()[self.section][theKey]) as d:
			if d.ShowModal() == wx.ID_CANCEL:
				return
			newValue = d.Value
		try:
			myConfig.modifyValue(self.section, theKey, newValue)
		except (KeyError, ValueError):
			# Translators: An error displayed when the modification fails.
			gui.messageBox(message = _("Can not modify the value."),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		except:
			log.debugWarning("", exc_info = True)
			# Translators: An error displayed when the modification fails.
			gui.messageBox(message = _("Can not modify the value."),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		self.topicsList.Selection = index
		self.topicsList.SetFocus()

	def onOpen(self, evt):
		if self.topicsList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the topics list.
			gui.messageBox(
			message = _("No selection found ! Please select an item in the list"),
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.topicsList.Selection
		key = self.topicsList.GetString(index)
		if self.section == "myApps":
			# We are looking to an application or directory.
				if os.path.isdir(myConfig.getConfig()[self.section][key]):
					# Is it a directory that we want to open?
					# We open our favorite directory.
					subprocess.call(['explorer', myConfig.getConfig()[self.section][key]])
				else:
					# No, it's an application.
					# We run our favorite application.
					subprocess.Popen(myConfig.getConfig()[self.section][key])
		elif self.section == "myContacts":
			# We are looking for a contact.
			# We display the phone number of the selected contact in a messageBox.
			gui.messageBox(message = _("The phone number of {theName} is {theNumber}").format(theName = key, theNumber = myConfig.getConfig()[self.section][key]), caption = _("The phone number"), style = wx.OK|wx.ICON_INFORMATION, parent = self)
		else:
			# We are looking for a journal website or a website.
			# We open our favorite website or journal website.
			webbrowser.open(myConfig.getConfig()[self.section][key])
		# You can comment this line if you prefer to leave the list of items available.
		self.Destroy()

	def onClose(self, evt):
		self.Destroy()

class NewElementDialog(wx.Dialog):

	def __init__(self, parent):
		# Translators: The title of the dialog to create a new element in the topics list.
		super(NewElementDialog, self).__init__(parent, title = _("New element"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a field to enter the name of a new element in the topics list.
		sizer.Add(wx.StaticText(self, label = _("Element name:")))
		item = self.elementName = wx.TextCtrl(self)
		sizer.Add(item)
		mainSizer.Add(sizer)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a field to enter the value of the new element.
		sizer.Add(wx.StaticText(self, label = _("Element value:")))
		item = self.elementValue = wx.TextCtrl(self)
		sizer.Add(item)
		mainSizer.Add(sizer)

		mainSizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		self.Bind(wx.EVT_BUTTON, self.onOk, id = wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id = wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.elementName.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onOk(self, evt):
		key = self.elementName.Value
		if key in myConfig.getConfig()[self.Parent.section].keys():
			# Translators: An error displayed when the key already exists.
			gui.messageBox(message = _("This name already exists. Please choose a different name"), caption = _("Error"), style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		myConfig.modifyValue(section = self.Parent.section, key = self.elementName.Value, value = self.elementValue.Value)
		self.Parent.onDisableOrEnableButtons()
		self.Parent.itemsList.append(self.elementName.GetValue())
		self.Parent.topicsList.Set(self.Parent.itemsList)
		self.Parent.topicsList.Selection = self.Parent.topicsList.FindString(self.elementName.Value)
		self.Parent.topicsList.SetFocus()

	def onCancel(self, evt):
		self.Destroy()
