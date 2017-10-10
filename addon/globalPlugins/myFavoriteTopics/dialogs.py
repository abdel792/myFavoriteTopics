# coding:utf-8

# globalPlugins/myFavoriteTopics/dialogs.py.

# Copyright 2017-2019 Abdelkrim Bensaïd and other contributors, released under gPL.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import configobj
import myConfig
import globalVars
import gui
import os
import webbrowser
import subprocess
import ui
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
		super(MyFavoriteTopicsDialog, self).__init__(parent = parent, title = _("My favorite topics"))
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
		item = wx.Button(parent = self, id = wx.ID_CLOSE, label = _("&Close"))
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
		evt.Skip()

	def onDisplayApps(self, evt):
		d = MyTopicsDialog(parent = self, section = "myApps")
		d.Show()
		evt.Skip()

	def onDisplayContacts(self, evt):
		d = MyTopicsDialog(parent = self, section = "myContacts")
		d.Show()
		evt.Skip()

	def onDisplayNews(self, evt):
		d = MyTopicsDialog(parent = self, section = "myNews")
		d.Show()
		evt.Skip()

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
		self.topics = topics
		# Translators: The title of the topics dialog.
		super(MyTopicsDialog, self).__init__(parent = parent, title = _("My {theTopics}").format(theTopics = topics[0]))
		self.itemsList = [self.onAddItemInformation(key) for key in myConfig.getConfig()[section].keys()]
		self.key = 1
		self.subsection = 2
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)

		# Translators: The label of the items list.
		sizer.Add(wx.StaticText(self, label = topics[1]))
		item = self.topicsList = wx.ListBox(self,
		choices = self.itemsList,
		style = wx.LB_SORT)

		item.Bind(wx.EVT_LISTBOX, self.onTopicsListChoice)
		sizer.Add(item)
		mainSizer.Add(sizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a button to open an element in the topics list.
		item = self.openButton = wx.Button(self, label = _("&Open"))
		item.Bind(wx.EVT_BUTTON, self.onOpen)
		item.SetDefault()
		sizer.Add(item)

		# Translators: The label of a button to create a new subsection in the topics list.
		item = self.addSubsectionButton = wx.Button(self, label = _("A&dd a new group"))
		item.Bind(wx.EVT_BUTTON, self.onNewSubsection)
		sizer.Add(item)

		# Translators: The label of a button to create a new key in the topics list, for the current section.
		item = self.addKeyButton = wx.Button(self, label = _("&Add a new key"))
		item.Bind(wx.EVT_BUTTON, self.onNewKey)
		sizer.Add(item)

		# Translators: The label of a button to rename an element in the topics list.
		item = self.renameElementButton = wx.Button(self, label = _("&Rename the key"))
		item.Bind(wx.EVT_BUTTON, self.onRenameElement)
		sizer.Add(item)

		# Translators: The label of a button to modify the value of a key in the topics list.
		item = self.modifyValueButton = wx.Button(self, label = _("&Modify value"))
		item.Bind(wx.EVT_BUTTON, self.onModifyValue)
		sizer.Add(item)

		# Translators: The label of a button to move the selected key to a group.
		item = self.moveButton = wx.Button(self, label = _("Mo&ve to group"))
		item.Bind(wx.EVT_BUTTON, self.onMoveToGroup)
		sizer.Add(item)

		# Translators: The label of a button to remove an item in the topics list.
		item = self.deleteButton = wx.Button(self, label = _("&Delete"))
		item.Bind(wx.EVT_BUTTON, self.onDelete)
		sizer.Add(item)
		mainSizer.Add(sizer)

		# Translators: The label of a button to close the dialog.
		item = wx.Button(parent = self, id = wx.ID_CLOSE, label = _("&Close"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(item)

		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE
		self.onDisableOrEnableButtons()
		self.selectFirstItem()

		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.topicsList.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def __del__(self):
		MyTopicsDialog._instance = None

	def onAddItemInformation(self, item):
		Group = _("(Group)")
		if not item:
			return
		if self.isGroup(item = item):
			item = unicode("{theItem} {section}", "utf-8").format(theItem = item, section = Group)
		return item

	def selectFirstItem(self):
		if self.topicsList.GetCount() > 0:
			self.topicsList.Selection = 0
			index = self.topicsList.Selection
			self.manageWidgets(index)

	def isGroup(self, index = None, item = None):
		key = item if item else self.topicsList.GetString(index).split(" (")[0]
		if isinstance(myConfig.getConfig()[self.section][key], configobj.Section):
			return True
		return False

	def adaptButtonsForGroup(self):
		self.renameElementButton.Label = _("&Rename the group")
		self.modifyValueButton.Disable()
		self.moveButton.Disable()

	def onTopicsListChoice(self, evt):
		index = self.topicsList.Selection
		self.manageWidgets(index)

	def manageWidgets(self, index):
		if self.isGroup(index = index):
			self.adaptButtonsForGroup()
		else:
			self.renameElementButton.Label = _("&Rename the key")
			self.modifyValueButton.Enabled = True
			if len(myConfig.getSubsectionsFromSection(section = self.section)) > 0:
				self.moveButton.Enabled = True
			else:
				self.moveButton.Enabled = False

	def onDisableOrEnableButtons(self):
		if globalVars.appArgs.secure:
			for item in self.openButton, self.addKeyButton, self.addSubsectionButton, self.renameElementButton, self.modifyValueButton, self.moveButton, self.deleteButton:
				item.Disable()
		else:
			for item in self.openButton, self.renameElementButton, self.modifyValueButton, self.moveButton, self.deleteButton:
				if len(myConfig.getConfig()[self.section].keys()) == 0:
					item.Disable()
				else:
					item.Enable()

	def onMoveToGroup(self, evt):
		choices = [key for key in myConfig.getSubsectionsFromSection(section = self.section)]
		choices.sort()
		index = self.topicsList.Selection
		item = self.topicsList.GetString(index)
		dlg = wx.SingleChoiceDialog(parent = self, message = _("Choose the group in {theTopic} topic, where you want to move {element}").format(theTopic = self.topics[0], element = item), caption = _("Move the element"), choices = choices)
		if dlg.ShowModal() == wx.ID_OK:
			if item in myConfig.getConfig()[self.section][dlg.GetStringSelection()].keys():
				# Translators: An error displayed when the key already exists.
				gui.messageBox(message = _("This name already exists. Please choose a different name"), caption = _("Error"), style = wx.OK|wx.ICON_ERROR, parent = self)
				return
			try:
				myConfig.modifyValue(section = self.section, key = item, value = myConfig.getConfig()[self.section][item], subsection = dlg.GetStringSelection())
				myConfig.delItem(section = self.section, key = item)
			except (KeyError, ValueError):
				# Translators: An error displayed when the move fails.
				gui.messageBox(message = _("Can not move {theItem}.").format(theItem = item),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
				return
			except:
				log.debugWarning("", exc_info = True)
				# Translators: An error displayed when the move fails.
				gui.messageBox(message = _("Can not move {theItem}.").format(theItem = item),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
				return
			del (self.itemsList[self.itemsList.index(item)])
			self.topicsList.Delete(index)
			self.topicsList.Selection = index - 1 if index == self.topicsList.GetCount() else index or 0
			if self.topicsList.GetCount() > 0:
				self.manageWidgets(self.topicsList.GetSelection())
			self.topicsList.SetFocus()
		else:
			self.manageWidgets(self.topicsList.GetSelection())
			dlg.Destroy()

	def onNewKey(self, evt):
		NewItemDialog(parent = self, item = self.key).Show()

	def onNewSubsection(self, evt):
		NewItemDialog(parent = self, item = self.subsection).Show()

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
		item = self.topicsList.GetString(index)
		key = item.split(" (")[0]
		try:
			myConfig.delItem(section = self.section, key = key)
		except:
			log.debugWarning("", exc_info = True)
			# Translators: An error displayed when deleting an element fails.
			gui.messageBox(message = _("Error deleting element."),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		self.onDisableOrEnableButtons()
		del self.itemsList[self.itemsList.index(item)]
		self.topicsList.Delete(index)
		self.topicsList.Selection = index - 1 if index == self.topicsList.GetCount() else index or 0
		if self.topicsList.GetCount() > 0:
			self.manageWidgets(self.topicsList.GetSelection())
		self.topicsList.SetFocus()

	def onRenameElement(self, evt):
		if self.topicsList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the topics list.
			gui.messageBox(
			message = _("No selection found ! Please select an item in the list"),
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.topicsList.Selection
		previousName = self.topicsList.GetString(index)
		oldName = previousName.split(" (")[0]
		fieldLabel = _("Rename the key") if not self.isGroup(item = oldName) else _("Rename the group")
		# Translators: The label of a field to enter a new name for the key or group.
		with wx.TextEntryDialog(parent = self, message = _("New name:"),
			# Translators: The title of the dialog to rename the key or group.
			caption = fieldLabel, defaultValue = oldName) as d:
			if d.ShowModal() == wx.ID_CANCEL:
				return
		newName = d.Value
		if newName == "":
			gui.messageBox(
			# Translators: An error displayed when the field is empty.
			message = _("You have not specified a new name for this item !"),
			caption = _("Error"),
			style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		if newName in myConfig.getConfig()[self.section].keys():
			# Translators: An error displayed when the key already exists.
			gui.messageBox(message = _("This name already exists. Please choose a different name"), caption = _("Error"), style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		try:
			myConfig.renameItem(section = self.section, oldKey = oldName, newKey = newName)
		except (KeyError, ValueError):
			# Translators: An error displayed when renaming a key fails.
			gui.messageBox(message = _("Can not rename this key or group."),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		except:
			log.debugWarning("", exc_info = True)
				# Translators: An error displayed when renaming a key fails.
			gui.messageBox(message = _("Error renaming key or group."),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		self.itemsList[self.itemsList.index(previousName)] = self.onAddItemInformation(newName)
		self.topicsList.Set(self.itemsList)
		self.topicsList.SetSelection(self.topicsList.FindString(self.onAddItemInformation(newName)))
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
		if self.section != "myContacts":
			# It's not a contact, wee don't need a multiline value.
			# Translators: The label of a field to enter a new value for the key.
			d = wx.TextEntryDialog(parent = self, message = _("New value:"), caption = _("Modify the value"), defaultValue = myConfig.getConfig()[self.section][theKey])
		else:
			# It's a contact, wee need a multiline value.
			# Translators: The label of a field to enter a new value for the key.
			d = wx.TextEntryDialog(parent = self, message = _("New value:"), caption = _("Modify the value"), defaultValue = myConfig.getConfig()[self.section][theKey], style = wx.TE_MULTILINE | wx.OK | wx.CANCEL)
		if d.ShowModal() == wx.ID_CANCEL:
			return
		newValue = d.Value
		try:
			myConfig.modifyValue(section = self.section, key = theKey, value = newValue)
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
		item = self.topicsList.GetString(index)
		if " (" in item:
			# We are looking to open a group and display the list of its items.
			MyGroupDialog(parent = self, section = self.section, subsection = item.split(" (")[0]).Show()
			return
		if self.section == "myApps":
			# We are looking to open an application or directory.
			try:
				if os.path.isdir(myConfig.getConfig()[self.section][item]):
					# Is it a directory that we want to open?
					# We open our favorite directory.
					subprocess.call(['explorer', myConfig.getConfig()[self.section][item]])
				else:
					# No, it's an application.
					# We run our favorite application.
					subprocess.Popen(myConfig.getConfig()[self.section][item])
			except:
				# Translators: An error displayed when opening the file or directory fails.
				gui.messageBox(message = _("Can not open {theItem}, this file or directory does not exist.").format(theItem = myConfig.getConfig()[self.section][item]),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		elif self.section == "myContacts":
			# We are looking for a contact.
			theValue = myConfig.getConfig()[self.section][item]
			information = unicode("{theName} {theInfos}", "utf-8").format(theName=item, theInfos=theValue)
			try:
				# We display the information of the selected contact in a wx.TextCtrl.
				d = DisplayContactInformationDialog(parent = self, text = information)
				d.Show()
			except:
			# Translators: An error displayed when opening the contact's information fails.
				gui.messageBox(message = _("Can not display {theItem}'s information.").format(theItem = item),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		else:
			# We are looking for a journal website or a website.
			try:
				# We open our favorite website or journal website.
				webbrowser.open(myConfig.getConfig()[self.section][item])
			except:
				# Translators: An error displayed when opening the url website or journal website fails.
				gui.messageBox(message = _("Can not open the url {theURL}.").format(theURL = myConfig.getConfig()[self.section][item]),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		# You can comment this line if you prefer to leave the list of items available.
		#self.Destroy()

	def onClose(self, evt):
		self.Destroy()

class NewItemDialog(wx.Dialog):

	def __init__(self, parent, item, noMain = None):
		self.noMain = noMain
		self.itemType = item
		fieldLabel = _("The group name:") if self.itemType == 2 else _("The key name:")
		# Translators: The title of the dialog to create a new item in the items list.
		super(NewItemDialog, self).__init__(parent = parent, title = fieldLabel)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a field to enter the name of a new item in the list.
		sizer.Add(wx.StaticText(self, label = _("Enter the name:")))
		item = self.itemName = wx.TextCtrl(self)
		sizer.Add(item)
		mainSizer.Add(sizer)
		if self.itemType == 1:
			sizer = wx.BoxSizer(wx.HORIZONTAL)
			# Translators: The label of a field to enter the value of the new key.
			sizer.Add(wx.StaticText(self, label = _("Key value:")))
			if self.Parent.section == "myContacts":
				item = self.itemValue = wx.TextCtrl(self, style = wx.TE_MULTILINE | wx.TE_RICH)
			else:
				item = self.itemValue = wx.TextCtrl(self)
			sizer.Add(item)
			mainSizer.Add(sizer)

		mainSizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		self.Bind(wx.EVT_BUTTON, self.onOk, id = wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id = wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.itemName.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onOk(self, evt):
		key = self.itemName.Value
		if key == "":
			gui.messageBox(
			# Translators: An error displayed when the field is empty.
			message = _("You have not specified a name for this item !"),
			caption = _("Error"),
			style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		if self.noMain:
			conf = myConfig.getConfig()[self.Parent.section][self.Parent.subsection]
		else:
			conf = myConfig.getConfig()[self.Parent.section]
		if key in conf.keys():
			# Translators: An error displayed when the key or group already exists.
			gui.messageBox(message = _("This name already exists. Please choose a different name"), caption = _("Error"), style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		if not self.noMain:
			if self.itemType == 2:
				conf = myConfig.getConfig()
				sb = conf[self.Parent.section][self.itemName.Value] = {}
				conf.write()
			else:
				myConfig.modifyValue(section = self.Parent.section, key = self.itemName.Value, value = self.itemValue.Value)
			self.Parent.itemsList.append(self.Parent.onAddItemInformation(self.itemName.Value))
			self.Parent.topicsList.Set(self.Parent.itemsList)
			self.Parent.topicsList.Selection = self.Parent.topicsList.FindString(self.Parent.onAddItemInformation(self.itemName.Value))
			self.Parent.onDisableOrEnableButtons()
			self.Parent.manageWidgets(self.Parent.topicsList.GetSelection())
			self.Parent.topicsList.SetFocus()
		else:
			myConfig.modifyValue(section = self.Parent.section, key = self.itemName.Value, value = self.itemValue.Value, subsection = self.Parent.subsection)
			self.Parent.itemsList.append(self.itemName.Value)
			self.Parent.keysList.Set(self.Parent.itemsList)
			self.Parent.keysList.Selection = self.Parent.keysList.FindString(self.itemName.Value)
			self.Parent.onDisableOrEnableButtons()
			self.Parent.manageWidgets(self.Parent.keysList.GetSelection())
			self.Parent.keysList.SetFocus()

	def onCancel(self, evt):
		self.Destroy()

class MyGroupDialog(wx.Dialog):

	def __init__(self, parent, section, subsection):
		self.section = section
		self.subsection = subsection

		# Translators: The title of the group dialog.
		super(MyGroupDialog, self).__init__(parent = parent, title = _("The group {theSubsection} of the {theSection} topic").format(theSubsection = subsection, theSection = parent.topics[0]))
		self.itemsList = []
		self.itemsList.extend(myConfig.getConfig()[self.section][self.subsection].keys())

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)

		# Translators: The label of the items list.
		sizer.Add(wx.StaticText(self, label = parent.topics[1]))
		item = self.keysList = wx.ListBox(self,
		choices = self.itemsList,
		style = wx.LB_SORT)

		item.Bind(wx.EVT_LISTBOX, self.onItemsListChoice)
		sizer.Add(item)
		mainSizer.Add(sizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a button to open an element in the items list.
		item = self.openButton = wx.Button(self, label = _("&Open"))
		item.Bind(wx.EVT_BUTTON, self.onOpen)
		item.SetDefault()
		sizer.Add(item)

		# Translators: The label of a button to create a new key in the items list, for the current group
		item = self.addKeyButton = wx.Button(self, label = _("&Add a new key"))
		item.Bind(wx.EVT_BUTTON, self.onNewKey)
		sizer.Add(item)

		# Translators: The label of a button to rename an element in the items list.
		item = self.renameKeyButton = wx.Button(self, label = _("&Rename the key"))
		item.Bind(wx.EVT_BUTTON, self.onRenameKey)
		sizer.Add(item)

		# Translators: The label of a button to modify the value of a key in the items list.
		item = self.modifyValueButton = wx.Button(self, label = _("&Modify value"))
		item.Bind(wx.EVT_BUTTON, self.onModifyValue)
		sizer.Add(item)

# Translators: The label of a button to move the selected key to a group.
		item = self.moveButton = wx.Button(self, label = _("Mo&ve to group"))
		item.Bind(wx.EVT_BUTTON, self.onMoveToGroup)
		sizer.Add(item)

		# Translators: The label of a button to remove an item in the items list.
		item = self.deleteButton = wx.Button(self, label = _("&Delete"))
		item.Bind(wx.EVT_BUTTON, self.onDelete)
		sizer.Add(item)
		mainSizer.Add(sizer)

		# Translators: The label of a button to close the dialog and return to main list.
		item = wx.Button(parent = self, id = wx.ID_CLOSE, label = _("Re&turn to main list"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(item)

		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE
		self.onDisableOrEnableButtons()
		self.selectFirstItem()

		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.keysList.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def selectFirstItem(self):
		if self.keysList.GetCount() > 0:
			self.keysList.Selection = 0
			index = self.keysList.Selection
			self.manageWidgets(index)

	def onItemsListChoice(self, evt):
		index = self.keysList.Selection
		self.manageWidgets(index = index)

	def manageWidgets(self, index):
		if len(myConfig.getSubsectionsFromSection(section = self.section)) > 1:
			self.moveButton.Enabled = True
		else:
			self.moveButton.Enabled = False

	def onDisableOrEnableButtons(self):
		if globalVars.appArgs.secure:
			for item in self.openButton, self.addKeyButton, self.renameKeyButton, self.modifyValueButton, self.moveButton, self.deleteButton:
				item.Disable()
		else:
			for item in self.openButton, self.renameKeyButton, self.modifyValueButton, self.moveButton, self.deleteButton:
				if len(myConfig.getConfig()[self.section][self.subsection].keys()) == 0:
					item.Disable()
				else:
					item.Enable()

	def onNewKey(self, evt):
		NewItemDialog(parent = self, item = 1, noMain = True).Show()

	def onDelete(self, evt):
		if self.keysList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the items list.
			gui.messageBox(
			message = _("No selection found ! Please select an item in the list"),
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.keysList.Selection
		if gui.messageBox(
			# Translators: The confirmation prompt displayed when the user requests to delete an element in the items list.
			message = _("Are you sure you want to delete {theKey}?").format(theKey = self.keysList.GetString(index)),
			# Translators: The title of the confirmation dialog for deletion of an element in the items list.
			caption = _("Confirm Deletion"),
			style = wx.YES | wx.NO | wx.ICON_QUESTION, parent = self
		) == wx.NO:
			return
		key = self.keysList.GetString(index)
		try:
			myConfig.delItem(section = self.section, key = key, subsection = self.subsection)
		except:
			log.debugWarning("", exc_info = True)
			# Translators: An error displayed when deleting an element fails.
			gui.messageBox(message = _("Error deleting element."),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		self.onDisableOrEnableButtons()
		del self.itemsList[self.itemsList.index(key)]
		self.keysList.Delete(index)
		self.keysList.Selection = index - 1 if index == self.keysList.GetCount() else index or 0
		self.keysList.SetFocus()

	def onRenameKey(self, evt):
		if self.keysList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the items list.
			gui.messageBox(
			message = _("No selection found ! Please select an item in the list"),
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.keysList.Selection
		oldName = self.keysList.GetString(index)
		# Translators: The label of a field to enter a new name for the key.
		with wx.TextEntryDialog(parent = self, message = _("New name:"),
				# Translators: The title of the dialog to rename the key.
				caption = _("Rename the key"), defaultValue = oldName) as d:
			if d.ShowModal() == wx.ID_CANCEL:
				return
		newName = d.Value
		if newName == "":
			gui.messageBox(
			# Translators: An error displayed when the field is empty.
			message = _("You have not specified a new name for this key !"),
			caption = _("Error"),
			style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		if newName in myConfig.getConfig()[self.section][self.subsection].keys():
			# Translators: An error displayed when the key already exists.
			gui.messageBox(message = _("This name already exists. Please choose a different name"), caption = _("Error"), style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		try:
			myConfig.renameItem(section = self.section, oldKey = oldName, newKey = newName, subsection = self.subsection)
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
		self.keysList.Set(self.itemsList)
		self.keysList.SetSelection(self.keysList.FindString(newName))
		self.keysList.SetFocus()

	def onModifyValue(self, evt):
		if self.keysList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the items list.
			gui.messageBox(
			message = _("No selection found ! Please select an item in the list"),
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.keysList.Selection
		theKey = self.keysList.GetString(index)
		if self.section != "myContacts":
			# It's not a contact, wee don't need a multiline value.
			# Translators: The label of a field to enter a new value for the key.
			d = wx.TextEntryDialog(parent = self, message = _("New value:"), caption = _("Modify the value"), defaultValue = myConfig.getConfig()[self.section][self.subsection][theKey])
		else:
			# It's a contact, wee need a multiline value.
			# Translators: The label of a field to enter a new value for the key.
			d = wx.TextEntryDialog(parent = self, message = _("New value:"), caption = _("Modify the value"), defaultValue = myConfig.getConfig()[self.section][self.subsection][theKey], style = wx.TE_MULTILINE | wx.OK | wx.CANCEL)
		if d.ShowModal() == wx.ID_CANCEL:
			return
		newValue = d.Value
		try:
			myConfig.modifyValue(section = self.section, key = theKey, value = newValue, subsection = self.subsection)
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
		self.keysList.Selection = index
		self.keysList.SetFocus()

	def onOpen(self, evt):
		if self.keysList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the items list.
			gui.messageBox(
			message = _("No selection found ! Please select an item in the list"),
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.keysList.Selection
		item = self.keysList.GetString(index)
		if self.section == "myApps":
			# We are looking for an application or directory.
			try:
				if os.path.isdir(myConfig.getConfig()[self.section][self.subsection][item]):
					# Is it a directory that we want to open?
					# We open our favorite directory.
					subprocess.call(['explorer', myConfig.getConfig()[self.section][self.subsection][item]])
				else:
					# No, it's an application.
					# We run our favorite application.
					subprocess.Popen(myConfig.getConfig()[self.section][self.subsection][item])
			except:
				# Translators: An error displayed when opening the file or directory fails.
				gui.messageBox(message = _("Can not open {theItem}, this file or directory does not exist.").format(theItem = myConfig.getConfig()[self.section][self.subsection][item]),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		elif self.section == "myContacts":
			theValue = myConfig.getConfig()[self.section][self.subsection][item]
			# We are looking for a contact.
			information = unicode("{theName} {theInfos}", "utf-8").format(theName=item, theInfos=theValue)
			try:
				# We display the information of the selected contact in a wx.TextCtrl.
				d = DisplayContactInformationDialog(parent = self, text = information)
				d.Show()
			except:
			# Translators: An error displayed when opening the contact's information fails.
				gui.messageBox(message = _("Can not display {theItem}'s information.").format(theItem = item),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		else:
			# We are looking for a journal website or a website.
			try:
				# We open our favorite website or journal website.
				webbrowser.open(myConfig.getConfig()[self.section][self.subsection][item])
			except:
				# Translators: An error displayed when opening the url website or journal website fails.
				gui.messageBox(message = _("Can not open the url {theURL}.").format(theURL = myConfig.getConfig()[self.section][self.subsection][item]),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		# You can comment this line if you prefer to leave the list of items available.
		#self.Destroy()

	def onMoveToGroup(self, evt):
		choices = [key for key in myConfig.getSubsectionsFromSection(section = self.section, exc = self.subsection)]
		choices.sort()
		index = self.keysList.Selection
		item = self.keysList.GetString(index)
		dlg = wx.SingleChoiceDialog(parent = self, message = _("Choose the group in {theTopic} topic, where you want to move {element}").format(theTopic = self.Parent.topics[0], element = item), caption = _("Move the element"), choices = choices)
		if dlg.ShowModal() == wx.ID_OK:
			if item in myConfig.getConfig()[self.section][dlg.GetStringSelection()].keys():
				# Translators: An error displayed when the key already exists.
				gui.messageBox(message = _("This name already exists. Please choose a different name"), caption = _("Error"), style = wx.OK|wx.ICON_ERROR, parent = self)
				return
			try:
				myConfig.modifyValue(section = self.section, key = item, value = myConfig.getConfig()[self.section][self.subsection][item], subsection = dlg.GetStringSelection())
				myConfig.delItem(section = self.section, key = item, subsection = self.subsection)
			except (KeyError, ValueError):
				# Translators: An error displayed when the move fails.
				gui.messageBox(message = _("Can not move {theItem}.").format(theItem = item),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
				return
			except:
				log.debugWarning("", exc_info = True)
				# Translators: An error displayed when the move fails.
				gui.messageBox(message = _("Can not move {theItem}.").format(theItem = item),
				caption = _("Error"), style = wx.OK | wx.ICON_ERROR, parent = self)
				return
			del (self.itemsList[self.itemsList.index(item)])
			self.keysList.Delete(index)
			self.keysList.Selection = index - 1 if index == self.keysList.GetCount() else index or 0
			self.onDisableOrEnableButtons()
			if self.keysList.GetCount() > 0:
				self.manageWidgets(self.keysList.GetSelection())
			self.keysList.SetFocus()
		else:
			self.manageWidgets(self.keysList.GetSelection())
			dlg.Destroy()

	def onClose(self, evt):
		self.Parent.manageWidgets(self.Parent.topicsList.GetSelection())
		self.Destroy()

class DisplayContactInformationDialog(wx.Dialog):

	def __init__(self, parent, text):
		# Translators: The title of the dialog to display the selected contact information.
		super(DisplayContactInformationDialog, self).__init__(parent = parent, title = _("Contact's information"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of the field that should display the contact's information.
		sizer.Add(wx.StaticText(self, label = _("Contact's information")))
		item = self.contactInformation = wx.TextCtrl(parent = self, value =text, style = wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH, size = (500, 200))
		item.SetBackgroundColour(wx.SystemSettings.GetColour(4))
		sizer.Add(item)
		item.SetFocus()

		# Translators: The label of a button to close the dialog.
		item = wx.Button(parent = self, id = wx.ID_CLOSE, label = _("&Close"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		sizer.Add(item)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE
		mainSizer.Add(sizer)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onClose(self, evt):
		self.Destroy()

