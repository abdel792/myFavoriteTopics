# coding:utf-8

# globalPlugins/myFavoriteTopics/dialogs.py.

# Copyright 2017-2019 Abdelkrim Bensaïd and other contributors, released under gPL.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import re
import configobj
from logHandler import log
from collections import OrderedDict
import sys
import os
from logHandler import log
if sys.version_info.major == 2:
	sys.path.append(os.path.join (os.path.abspath(os.path.dirname(__file__)), "libPy2"))
	try:
		from bs4 import BeautifulSoup
		from googlesearch import search
	except Exception as e:
		log.debugWarning(e, exc_info = True)
else:
	sys.path.insert(0, os.path.join (os.path.abspath(os.path.dirname(__file__)), "libPy3"))
	try:
		from bs4 import BeautifulSoup
		from googlesearch import search
	except Exception as e:
		log.debugWarning(e, exc_info = True)
sys.path.remove(sys.path[-1] if sys.version_info.major == 2 else sys.path[0])
from . import myConfig
import globalVars
import gui
import webbrowser
import subprocess
import ui
import queueHandler
if sys.version_info.major == 2:
	import urllib
	from . import urllib2
else:
	import urllib
import random

# For translation.
import addonHandler
addonHandler.initTranslation()

#list of fake user agent
userAgentList=['Mozilla/5.0', 'Safari/537.36', 'Chrome/67.0.3396.99', 'iexplore/11.0.9600.19080', 'Trident/7.0', 'SeaMonkey/2.40', 'Wyzo/3.6.4.1', 'OPR/54.0.2952.64']

def google_scrape(url):
	request= urllib2.Request(url) if sys.version_info.major == 2 else urllib.request.Request(url)
	request.add_header('User-Agent', random.choice(userAgentList))
	handle = urllib2.urlopen(request) if sys.version_info.major == 2 else urllib.request.urlopen(request)
	page= handle.read().decode('utf-8')
	soup = BeautifulSoup(page, "html.parser")
	return soup.title.text

def deNoise(text):
	"""
	From : https://alraqmiyyat.github.io/2013/01-02.html
	"""
	
	noise = re.compile(u"""ّ|# Tashdid
		َ|# Fatha
		ً|# Tanwin Fath
		ُ|# Damma
		ٌ|# Tanwin Damm
		ِ|# Kasra
		ٍ|# Tanwin Kasr
		ْ|# Sukun
		ـ# Tatwil/Kashida
		""", re.U | re.VERBOSE)
	text = re.sub(noise, u'', text, re.U)
	return text

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
		super(MyFavoriteTopicsDialog, self).__init__(parent = parent,
		# Translators: The title of the favorite topics dialog.
		title = _("My favorite topics"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)

		item = self.googleSearchButton = wx.Button(self,
		# Translators: The label of a button to do a search on Google or Youtube.
		label = _("Sea&rch on Google or Youtube"))
		item.Bind(wx.EVT_BUTTON, self.onGoogleSearch)
		sizer.Add(item)

		item = self.websitesListButton = wx.Button(self,
		# Translators: The label of a button to display the list of the favorite websites.
		label = _("Display my favorite &websites"))
		item.Bind(wx.EVT_BUTTON, self.onDisplayWebsites)
		sizer.Add(item)

		item = self.appsListButton = wx.Button(self,
		# Translators: The label of a button to display the list of the favorite applications or directories.
		label = _("Display my favorite &applications"))
		item.Bind(wx.EVT_BUTTON, self.onDisplayApps)
		sizer.Add(item)

		item = self.contactsListButton = wx.Button(self,
		# Translators: The label of a button to display the list of the favorite contacts.
		label = _("Display my favorite &contacts"))
		item.Bind(wx.EVT_BUTTON, self.onDisplayContacts)
		sizer.Add(item)

		item = self.newsListButton = wx.Button(self,
		# Translators: The label of a button to display the list of the favorite journal websites.
		label = _("Display my favorite &journal websites"))
		item.Bind(wx.EVT_BUTTON, self.onDisplayNews)
		sizer.Add(item)

		item = self.notesListButton = wx.Button(self,
		# Translators: The label of a button to display the list of the saved notes.
		label = _("Display my &notes"))
		item.Bind(wx.EVT_BUTTON, self.onDisplayNotes)
		sizer.Add(item)

		mainSizer.Add(sizer)
		item = wx.Button(parent = self, id = wx.ID_CLOSE,
		# Translators: The label of a button to close the dialog.
		label = _("&Close"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(item)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE

		if globalVars.appArgs.secure:
			for item in self.googleSearchButton, self.websitesListButton, self.appsListButton, self.contactsListButton, self.newsListButton, self.notesListButton:
				item.Disable()
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def __del__(self):
		MyFavoriteTopicsDialog._instance = None

	def onGoogleSearch (self, evt):
		TextEntryDialog (parent = self,
		# Translators: The title of the edit field.
		title = _("Enter your search"),
		# Translators: The label of the edit field.
		fieldLabel = _("Search:"),
		item = 5).Show()
		evt.Skip()

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

	def onDisplayNotes(self, evt):
		d = MyTopicsDialog(parent = self, section = "myNotes")
		d.Show()
		evt.Skip()

	def onClose(self, evt):
		self.Destroy()
		MyFavoriteTopicsDialog._instance = None

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
		self.contact = False
		self.notes = False
		self.section = section
		if section == "mySites":
			topics = [
			# Translators: The title of the topics dialog.
			_("favorite websites"),
			# Translators: The label of the topics list.
			_("Websites")
			]
		elif section == "myApps":
			topics = [
			# Translators: The title of the topics dialog.
			_("favorite applications or directories"),
			# Translators: The label of the topics list.
			_("Applications or directories")
			]
		elif section == "myContacts":
			self.contact = True
			topics = [
			# Translators: The title of the topics dialog.
			_("favorite contacts"),
			# Translators: The label of the topics list.
			_("Contacts")
			]
		elif section == "myNews":
			topics = [
			# Translators: The title of the topics dialog.
			_("favorite journal websites"),
			# Translators: The label of the topics list.
			_("journal websites")
			]
		elif section == "myNotes":
			self.notes = True
			topics = [
			# Translators: The title of the topics dialog.
			_("Saved notes"),
			# Translators: The label of the topics list.
			_("Notes")
			]
		self.topics = topics
		super(MyTopicsDialog, self).__init__(parent = parent, title = _("My {theTopics}").format(theTopics = topics[0]))
		self.itemsList = [self.onAddItemInformation(key) for key in myConfig.getConfig()[section].keys()]
		self.element = 1
		self.group = 2
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(wx.StaticText(self, label = topics[1]))
		item = self.topicsList = wx.ListBox(self,
		choices = self.itemsList,
		style = wx.LB_SORT)

		item.Bind(wx.EVT_LISTBOX, self.onTopicsListChoice)
		sizer.Add(item)
		mainSizer.Add(sizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		item = self.openButton = wx.Button(self,
		# Translators: The label of a button to open an element in the topics list.
		label = _("&Open"))
		item.Bind(wx.EVT_BUTTON, self.onOpen)
		item.SetDefault()
		sizer.Add(item)

		item = self.addGroupButton = wx.Button(self,
		# Translators: The label of a button to create a new group in the topics list.
		label = _("A&dd a new group"))
		item.Bind(wx.EVT_BUTTON, self.onNewGroup)
		sizer.Add(item)

		item = self.addElementButton = wx.Button(self,
		# Translators: The label of a button to create a new element in the topics list, for the current section.
		label = _("&Add a new element"))
		item.Bind(wx.EVT_BUTTON, self.onNewElement)
		sizer.Add(item)

		item = self.renameElementButton = wx.Button(self,
		# Translators: The label of a button to rename an element in the topics list.
		label = _("&Rename the element"))
		item.Bind(wx.EVT_BUTTON, self.onRenameElement)
		sizer.Add(item)

		item = self.modifyValueButton = wx.Button(self,
		# Translators: The label of a button to modify the value of an element in the topics list.
		label = _("&Modify value"))
		item.Bind(wx.EVT_BUTTON, self.onModifyValue)
		sizer.Add(item)

		item = self.moveButton = wx.Button(self,
		# Translators: The label of a button to move the selected element to a group.
		label = _("Mo&ve to group"))
		item.Bind(wx.EVT_BUTTON, self.onMoveToGroup)
		sizer.Add(item)

		if self.contact or self.notes:
			item = self.findButton = wx.Button(self,
			# Translators: The label of a button to find a contact or note.
			label = _("&Find"))
			item.Bind(wx.EVT_BUTTON, self.onFindButton)
			sizer.Add(item)			

		item = self.deleteButton = wx.Button(self,
		# Translators: The label of a button to remove an item in the topics list.
		label = _("&Delete"))
		item.Bind(wx.EVT_BUTTON, self.onDelete)
		sizer.Add(item)
		mainSizer.Add(sizer)

		item = wx.Button(parent = self, id = wx.ID_CLOSE,
		# Translators: The label of a button to close the dialog.
		label = _("&Close"))
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
			item = unicode("{theItem} {section}", "utf-8").format(theItem = item, section = Group) if sys.version_info.major == 2 else "{theItem} {section}".format(theItem = item, section = Group)
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
		# Translators: The label of the button for renaming the group.
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
			# Translators: The label of the button for renaming the element.
			self.renameElementButton.Label = _("&Rename the element")
			self.modifyValueButton.Enabled = True
			if len(myConfig.getSubsectionsFromSection(section = self.section)) > 0:
				self.moveButton.Enabled = True
			else:
				self.moveButton.Enabled = False

	def onDisableOrEnableButtons(self):
		if globalVars.appArgs.secure:
			for item in self.openButton, self.addElementButton, self.addGroupButton, self.renameElementButton, self.modifyValueButton, self.moveButton, self.findButton, self.deleteButton:
				item.Disable()
		else:
			if self.contact or self.notes:
				for item in self.openButton, self.renameElementButton, self.modifyValueButton, self.moveButton, self.findButton, self.deleteButton:
					if len(myConfig.getConfig()[self.section].keys()) == 0:
						item.Disable()
					else:
						item.Enable()
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
		dlg = wx.SingleChoiceDialog(parent = self,
		# Translators: The message prompting the user to choose a group to move the element.
		message = _("Choose the group in {theTopic} topic, where you want to move {element}").format(theTopic = self.topics[0], element = item),
		# Translators: The caption of the dialog prompting the user to move the element to a group.
		caption = _("Move the element"),
		choices = choices)
		if dlg.ShowModal() == wx.ID_OK:
			if item in myConfig.getConfig()[self.section][dlg.GetStringSelection()].keys():
				gui.messageBox(
				# Translators: An error displayed when the element already exists.
				message = _("This name already exists. Please choose a different name"),
				# Translators: the caption of the error message.
				caption = _("Error"),
				style = wx.OK|wx.ICON_ERROR, parent = self)
				return
			try:
				myConfig.modifyValue(section = self.section, key = item, value = myConfig.getConfig()[self.section][item], subsection = dlg.GetStringSelection())
				myConfig.delItem(section = self.section, key = item)
			except (KeyError, ValueError):
				gui.messageBox(
				# Translators: An error displayed when the move fails.
				message = _("Can not move {theItem}.").format(theItem = item),
				# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
				return
			except:
				log.debugWarning("", exc_info = True)
				gui.messageBox(
				# Translators: An error displayed when the move fails.
				message = _("Can not move {theItem}.").format(theItem = item),
				# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
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

	def onNewElement(self, evt):
		TextEntryDialog(parent = self,
		# Translators: The title of the edit field.
		title = _("The element name:"),
		# Translators: The label of the edit field.
		fieldLabel = _("Enter your element name"),
		item = self.element).Show()

	def onNewGroup(self, evt):
		TextEntryDialog(parent = self,
		# Translators: The title of the edit field.
		title = _("The group name:"),
		# Translators: The label of the edit field.
		fieldLabel = _("Enter your group name"),
		item = self.group).Show()

	def onDelete(self, evt):
		if self.topicsList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the topics list.
			gui.messageBox(
			# Translators: An error message indicating that no selection has been made.
			message = _("No selection found ! Please select an item in the list"),
			# Translators: The caption of the error message.
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
			gui.messageBox(
			# Translators: An error message indicating that the deletion cannot be performed.
			message = _("Error deleting element."),
			# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
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
			# Translators: An error message indicating that no selection has been made.
			message = _("No selection found ! Please select an item in the list"),
			# Translators: The caption of the error message.
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.topicsList.Selection
		previousName = self.topicsList.GetString(index)
		oldName = previousName.split(" (")[0]
		# Translators: The label of the edit field prompting the user to rename the group or element.
		fieldLabel = _("Rename the element") if not self.isGroup(item = oldName) else _("Rename the group")
		with wx.TextEntryDialog(self, _("New name:"),
			# Translators: The title of the dialog to rename the element or group.
			fieldLabel, oldName) as d:
			if d.ShowModal() == wx.ID_CANCEL:
				return
		newName = d.Value
		if newName == "":
			gui.messageBox(
			# Translators: An error displayed when the field is empty.
			message = _("You have not specified a value for this field !"),
			# Translators: The caption of the error message.
			caption = _("Error"),
			style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		if newName in myConfig.getConfig()[self.section].keys():
			gui.messageBox(
			# Translators: An error displayed when the element already exists.
			message = _("This name already exists. Please choose a different name"),
			# Translators: The caption of the error message.
			caption = _("Error"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		try:
			myConfig.renameItem(section = self.section, oldKey = oldName, newKey = newName)
		except (KeyError, ValueError):
			gui.messageBox(
			# Translators: An error displayed when renaming an element fails.
			message = _("Can not rename this element or group."),
			# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		except:
			log.debugWarning("", exc_info = True)
			gui.messageBox(
				# Translators: An error displayed when renaming an element fails.
			message = _("Error renaming element or group."),
			# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		self.itemsList[self.itemsList.index(previousName)] = self.onAddItemInformation(newName)
		self.topicsList.Set(self.itemsList)
		self.topicsList.SetSelection(self.topicsList.FindString(self.onAddItemInformation(newName)))
		self.topicsList.SetFocus

	def onModifyValue(self, evt):
		if self.topicsList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the topics list.
			gui.messageBox(
			# Translators: An error message indicating that no selection has been made.
			message = _("No selection found ! Please select an item in the list"),
			# Translators: The caption of the error message.
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.topicsList.Selection
		theKey = self.topicsList.GetString(index)
		if self.section != "myContacts" and self.section != "myNotes":
			# It's not a contact or note, wee don't need a multiline value.
			d = wx.TextEntryDialog(self,
			# Translators: The label of a field to enter a new value for the element.
			_("New value:"),
			# Translators: The title of the edit field prompting the user to enter a new value.
			_("Modify the value"),
			myConfig.getConfig()[self.section][theKey])
		else:
			# It's a contact or note, wee need a multiline value.
			d = wx.TextEntryDialog(self,
			# Translators: The label of a field to enter a new value for the element.
			_("New value:"),
			# Translators: The title of the edit field prompting the user to enter a new value.
			_("Modify the value"),
			myConfig.getConfig()[self.section][theKey], style = wx.TE_MULTILINE | wx.OK | wx.CANCEL)
		if d.ShowModal() == wx.ID_CANCEL:
			return
		newValue = d.Value
		try:
			myConfig.modifyValue(section = self.section, key = theKey, value = newValue)
		except (KeyError, ValueError):
			gui.messageBox(
			# Translators: An error displayed when the modification fails.
			message = _("Can not modify the value."),
			# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		except:
			log.debugWarning("", exc_info = True)
			gui.messageBox(
			# Translators: An error displayed when the modification fails.
			message = _("Can not modify the value."),
			# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		self.topicsList.Selection = index
		self.topicsList.SetFocus()

	def onOpen(self, evt):
		if self.topicsList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the topics list.
			gui.messageBox(
			# Translators: An error message indicating that no selection has been made.
			message = _("No selection found ! Please select an item in the list"),
			# Translators: The caption of the error message.
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
				gui.messageBox(
				# Translators: An error displayed when opening the file or directory fails.
				message = _("Can not open {theItem}, this file or directory does not exist.").format(theItem = myConfig.getConfig()[self.section][item]),
				# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		elif self.section == "myContacts":
			# We are looking for a contact.
			theValue = myConfig.getConfig()[self.section][item]
			information = unicode("{theName} {theInfos}", "utf-8").format(theName=item, theInfos=theValue) if sys.version_info.major == 2 else "{theName} {theInfos}".format(theName=item, theInfos=theValue)
			try:
				# We display the information of the selected contact in a wx.TextCtrl.
				d = DisplayInformationDialog(parent = self, text = information)
				d.Show()
			except:
				gui.messageBox(
				# Translators: An error displayed when opening the contact's information fails.
				message = _("Can not display {theItem}'s information.").format(theItem = item),
				# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		elif self.section == "myNotes":
			# We are looking for a note.
			theValue = myConfig.getConfig()[self.section][item]
			information = unicode("{theName} {theInfos}", "utf-8").format(theName=item, theInfos=theValue) if sys.version_info.major == 2 else "{theName} {theInfos}".format(theName=item, theInfos=theValue)
			try:
				# We display the information of the selected note in a wx.TextCtrl.
				d = DisplayInformationDialog(parent = self, text = information)
				d.Show()
			except:
				gui.messageBox(
				# Translators: An error displayed when opening the informations of the note fails.
				message = _("Can not display {theItem}'s information.").format(theItem = item),
				# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		else:
			# We are looking for a journal website or a website.
			try:
				# We open our favorite website or journal website.
				webbrowser.open(myConfig.getConfig()[self.section][item])
			except:
				gui.messageBox(
				# Translators: An error displayed when opening the url website or journal website fails.
				message = _("Can not open the url {theURL}.").format(theURL = myConfig.getConfig()[self.section][item]),
				# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		# You can comment this line if you prefer to leave the list of items available.
		#self.Destroy()

	def onFindButton (self, evt):
		d=TextEntryDialog(parent = self,
		# Translators: The title of the edit field.
		title=_("Search a contact:") if self.contact else _("Search a note:"),
		# Translators: The label of the edit field.
		fieldLabel = _("Enter some information about the contact that you are looking for") if self.contact else _("Enter some information about the note that you are looking for"),
		item = 3 if self.contact else 4)
		d.Show()

	def onClose(self, evt):
		self.Destroy()
		MyTopicsDialog._instance = None

class TextEntryDialog(wx.Dialog):

	def __init__(self, parent, title, fieldLabel, item, noMain = None):
		self.noMain = noMain
		self.itemType = item
		# Translators: The title of the html message.
		self.searchResultTitle = _("Search results:")
		self.searchContact = 3
		self.searchNote = 4
		self.googleSearch = 5
		super(TextEntryDialog, self).__init__(parent = parent, title = title)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(wx.StaticText(self, label = fieldLabel))
		item = self.itemName = wx.TextCtrl(self)
		sizer.Add(item)
		mainSizer.Add(sizer)
		if self.itemType == 1:
			sizer = wx.BoxSizer(wx.HORIZONTAL)
			sizer.Add(wx.StaticText(self,
			# Translators: The label of a field to enter the value of the new element.
			label = _("Element value:")))
			if self.Parent.section == "myContacts" or self.Parent.section == "myNotes":
				item = self.itemValue = wx.TextCtrl(self, style = wx.TE_MULTILINE | wx.TE_RICH)
			else:
				item = self.itemValue = wx.TextCtrl(self)
			sizer.Add(item)
			mainSizer.Add(sizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		item = self.validateButton = wx.Button(self, id = wx.ID_OK,
		# Translators: The label of a button to validate the dialog.
		label = _("&Validate") if self.itemType < self.googleSearch else _("Search and &display in html message"))
		item.Bind(wx.EVT_BUTTON, self.onValidate)
		sizer.Add(item)
		item.SetDefault()

		if self.itemType > 4:
			item = self.displayInBrowserButton = wx.Button(self,
			# Translators: The label of a button to display the Google or Youtube result with the browser.
			label = _("Display on &browser"))
			item.Bind(wx.EVT_BUTTON, self.onDisplayOnBrowser)
			sizer.Add(item)

		item = self.cancelButton = wx.Button(self, id = wx.ID_CANCEL,
		# Translators: The label of a button to cancel the dialog.
		label = _("&Cancel"))
		item.Bind(wx.EVT_BUTTON, self.onCancel)
		sizer.Add(item)
		mainSizer.Add(sizer)
		self.Bind(wx.EVT_BUTTON, self.onValidate, id = wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id = wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.itemName.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onValidate(self, evt):
		key = self.itemName.Value
		if key == "":
			gui.messageBox(
			# Translators: An error displayed when the field is empty.
			message = _("You have not specified a value for this field !"),
			# Translators: The caption of the error message.
			caption = _("Error"),
			style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		if self.itemType == self.googleSearch:
			html = ""
			i = 1
			query = key.encode("utf-8") if sys.version_info.major == 2 else key
			for url in search(query, stop=20):
				a = google_scrape(url)
				html += '<h3>{0}-<a href="{1}">{2}</a></h3>'.format(str(i), url, a)
				i += 1
			queueHandler.queueFunction (queueHandler.eventQueue, ui.browseableMessage, message = html,
			title = self.searchResultTitle,
			isHtml = True)
			return
		if self.noMain:
			conf = myConfig.getConfig()[self.Parent.section][self.Parent.subsection]
		else:
			conf = myConfig.getConfig()[self.Parent.section]
		if self.itemType == self.searchContact:
			infos = ""
			found = False
			dct = OrderedDict (sorted(conf.items(), key=lambda x: x[0].lower()))
			for item in dct:
				if isinstance(dct[item], configobj.Section):
					sortedDict = OrderedDict(sorted(conf[item].items(), key=lambda k: k[0].lower()))
					for element in sortedDict:
						if re.search (u"\\b" + deNoise(key) + u"\\b", deNoise(element), re.I | re.U):
							infos += u"<h1>{0} {1}</h1>\r\n".format(_("Group:"), item)
							infos += u"<h2>{0}</h2>\r\n".format(element)
							i = 0
							content = []
							suite = sortedDict[element].split("\n")
							for line in suite:
								content.append(line)
								i += 1
								if i == 6:
									break
							infos += u"<pre>{0}</pre>\r\n".format("\r\n".join(content))
						if re.search (u"\\b" + deNoise(key) + u"\\b", deNoise(sortedDict[element]), re.I | re.U):
							infos += u"<h1>{0} {1}</h1>\r\n".format(_("Group:"), item)
							infos += u"<h2>{0}</h2>\r\n".format(element)
							for m in re.finditer (u"\\b" + deNoise(key) + u"\\b", deNoise(sortedDict[element]), re.I | re.U):
								start = m.start()
								end = m.end()
								startOfLine = start - deNoise(sortedDict[element])[:start][::-1].find("\n") if deNoise(sortedDict[element])[:start][::-1].find("\n") != -1 else 0
								endOfLine = end + deNoise(sortedDict[element])[end:].find("\n") if deNoise(sortedDict[element])[end:].find("\n") != -1 else len(deNoise(sortedDict[element]))
								i = 0
								content = []
								suite = deNoise(sortedDict[element])[endOfLine:].split("\n")
								for line in suite:
									content.append(line)
									i += 1
									if i == 6:
										break
								infos += u"<h3>{0}</h3><pre>{1}</pre>\r\n".format(deNoise(sortedDict[element])[startOfLine:endOfLine], "\r\n".join(content))
			for item in dct:
				if not isinstance(dct[item], configobj.Section):
					if re.search (u"\\b" + deNoise(key) + u"\\b", deNoise(item), re.I | re.U):
						infos += u"<h1>{0}</h1>\r\n".format(item)
						i = 0
						content = []
						suite = conf[item].split("\n")
						for line in suite:
							content.append(line)
							i += 1
							if i == 6:
								break
						infos += u"<pre>{0}</pre>\r\n".format("\r\n".join(content))
					if re.search (u"\\b" + deNoise(key) + u"\\b", deNoise(conf[item]), re.I | re.U):
						infos += u"<h1>{0}</h1>\r\n".format(item)
						for m in re.finditer ("\\b" + deNoise(key) + "\\b", deNoise(conf[item]), re.I | re.U):
							start = m.start()
							end = m.end()
							startOfLine = start - deNoise(conf[item])[:start][::-1].find("\n") if deNoise(conf[item])[:start][::-1].find("\n") != -1 else 0
							endOfLine = end + deNoise(conf[item])[end:].find("\n") if deNoise(conf[item])[end:].find("\n") != -1 else len(deNoise(conf[item]))
							i = 0
							content = []
							suite = deNoise(conf[item])[endOfLine:].split("\n")
							for line in suite:
								content.append(line)
								i += 1
								if i == 6:
									break
							infos += u"<h2>{0}</h2><pre>{1}</pre>\r\n".format(deNoise(conf[item])[startOfLine:endOfLine], "\r\n".join(content))
			self.Destroy()
			queueHandler.queueFunction(queueHandler.eventQueue, ui.browseableMessage, message=infos,
			title = self.searchResultTitle,
			isHtml=True)
			return
		if self.itemType == self.searchNote:
			infos = ""
			found = False
			dct = OrderedDict (sorted(conf.items(), key=lambda x: x[0].lower()))
			for item in dct:
				if isinstance(dct[item], configobj.Section):
					sortedDict = OrderedDict(sorted(conf[item].items(), key=lambda k: k[0].lower()))
					for element in sortedDict:
						if deNoise(key.lower()) in deNoise(element.lower()) or deNoise(key.lower()) in deNoise(sortedDict[element].lower()):
							infos += u"<h1>{0} {1}</h1>\r\n".format(_("Group:"), item)
							infos += u"<h2>{0}</h2>\r\n".format(element)
							infos += u"<pre>{0}</pre>\r\n".format(sortedDict[element])
			for item in dct:
				if not isinstance(dct[item], configobj.Section):
					if deNoise(key.lower()) in deNoise(item.lower()) or deNoise(key.lower()) in deNoise(conf[item].lower()):
						infos += u"<h1>{0}</h1>\r\n".format(item)
						infos += u"<pre>{0}</pre>\r\n".format(conf[item])
			self.Destroy()
			queueHandler.queueFunction(queueHandler.eventQueue, ui.browseableMessage, message=infos,
			title = self.searchResultTitle,
			isHtml=True)
			return
		if key in conf.keys():
			gui.messageBox(
			# Translators: An error displayed when the element or group already exists.
			message = _("This name already exists. Please choose a different name"),
			# Translators: The caption of the error message.
			caption = _("Error"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		if not self.noMain:
			if self.itemType == self.Parent.group:
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

	def onDisplayOnBrowser (self, evt):
		terms = "+".join(self.itemName.Value.split())
		terms = urllib.quote(terms) if sys.version_info.major == 2 else urllib.parse.quote(terms)
		url = "http://www.google.fr/search?q={0}&lr=lang_ar&hl=fr&ie=utf-8&oe=utf-8".format(terms)
		webbrowser.open(url)

	def onCancel(self, evt):
		self.Destroy()

class MyGroupDialog(wx.Dialog):

	def __init__(self, parent, section, subsection):
		self.section = section
		self.subsection = subsection

		super(MyGroupDialog, self).__init__(parent = parent,
		# Translators: The title of the group dialog.
		title = _("The group {theSubsection} of the {theSection} topic").format(theSubsection = subsection, theSection = parent.topics[0]))
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
		item = self.openButton = wx.Button(self,
		# Translators: The label of a button to open an element in the items list.
		label = _("&Open"))
		item.Bind(wx.EVT_BUTTON, self.onOpen)
		item.SetDefault()
		sizer.Add(item)

		item = self.addKeyButton = wx.Button(self,
		# Translators: The label of a button to create a new key in the items list, for the current group.
		label = _("&Add a new element"))
		item.Bind(wx.EVT_BUTTON, self.onNewKey)
		sizer.Add(item)

		item = self.renameKeyButton = wx.Button(self,
		# Translators: The label of a button to rename an element in the items list.
		label = _("&Rename the element"))
		item.Bind(wx.EVT_BUTTON, self.onRenameKey)
		sizer.Add(item)

		item = self.modifyValueButton = wx.Button(self,
		# Translators: The label of a button to modify the value of an element in the items list.
		label = _("&Modify value"))
		item.Bind(wx.EVT_BUTTON, self.onModifyValue)
		sizer.Add(item)

		item = self.moveButton = wx.Button(self,
		# Translators: The label of a button to move the selected element to a group.
		label = _("Mo&ve to group"))
		item.Bind(wx.EVT_BUTTON, self.onMoveToGroup)
		sizer.Add(item)

		item = self.deleteButton = wx.Button(self,
		# Translators: The label of a button to remove an item in the items list.
		label = _("&Delete"))
		item.Bind(wx.EVT_BUTTON, self.onDelete)
		sizer.Add(item)
		mainSizer.Add(sizer)

		item = wx.Button(parent = self, id = wx.ID_CLOSE,
		# Translators: The label of a button to close the dialog and return to main list.
		label = _("Re&turn to main list"))
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
		TextEntryDialog(parent = self,
		# Translators: The title of the edit field.
		title = _("The element name:"),
		# Translators: The label of the edit field.
		fieldLabel = _("Your element name"),
		item = 1, noMain = True).Show()

	def onDelete(self, evt):
		if self.keysList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the items list.
			gui.messageBox(
			# Translators: An error  message indicating that no selection has been made.
			message = _("No selection found ! Please select an item in the list"),
			# Translators: The caption of the error message.
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
			gui.messageBox(
			# Translators: An error displayed when deleting an element fails.
			message = _("Error deleting element."),
			# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		self.onDisableOrEnableButtons()
		del self.itemsList[self.itemsList.index(key)]
		self.keysList.Delete(index)
		self.keysList.Selection = index - 1 if index == self.keysList.GetCount() else index or 0
		self.keysList.SetFocus()

	def onRenameKey(self, evt):
		if self.keysList.Selection == wx.NOT_FOUND:
			gui.messageBox(
			# Translators: An error message indicating that no selection has been made.
			message = _("No selection found ! Please select an item in the list"),
			# Translators: The caption of the error message.
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.keysList.Selection
		oldName = self.keysList.GetString(index)
		with wx.TextEntryDialog(self,
		# Translators: The label of a field to enter a new name for the element.
		_("New name:"),
				# Translators: The title of the dialog to rename the element.
				_("Rename the key"), oldName) as d:
			if d.ShowModal() == wx.ID_CANCEL:
				return
		newName = d.Value
		if newName == "":
			gui.messageBox(
			# Translators: An error displayed when the field is empty.
			message = _("You have not specified a value for this field!"),
			# Translators: The caption of the error message.
			caption = _("Error"),
			style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		if newName in myConfig.getConfig()[self.section][self.subsection].keys():
			gui.messageBox(
			# Translators: An error displayed when the element already exists.
			message = _("This name already exists. Please choose a different name"),
			# Translators: The caption of the error message.
			caption = _("Error"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		try:
			myConfig.renameItem(section = self.section, oldKey = oldName, newKey = newName, subsection = self.subsection)
		except (KeyError, ValueError):
			gui.messageBox(
			# Translators: An error displayed when renaming an element fails.
			message = _("Can not rename this element."),
			# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		except:
			log.debugWarning("", exc_info = True)
			gui.messageBox(
			# Translators: An error displayed when renaming an element fails.
			message = _("Error renaming element."),
			# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		self.itemsList[self.itemsList.index(oldName)] = newName
		self.keysList.Set(self.itemsList)
		self.keysList.SetSelection(self.keysList.FindString(newName))
		self.keysList.SetFocus()

	def onModifyValue(self, evt):
		if self.keysList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the items list.
			gui.messageBox(
			# Translators: An error message indicating that no selection has been made.
			message = _("No selection found ! Please select an item in the list"),
			# Translators: The caption of the error message.
			caption = _("No selection"),
			style = wx.OK|wx.ICON_ERROR, parent = self)
			return
		index = self.keysList.Selection
		theKey = self.keysList.GetString(index)
		if self.section != "myContacts" and self.section != "myNotes":
			# It's not a contact or note, wee don't need a multiline value.
			d = wx.TextEntryDialog(self,
			# Translators: The label of a field to enter a new value for the element.
			_("New value:"), _("Modify the value"),
			myConfig.getConfig()[self.section][self.subsection][theKey])
		else:
			# It's a contact or note, wee need a multiline value.
			d = wx.TextEntryDialog(self,
			# Translators: The label of a field to enter a new value for the element.
			_("New value:"), _("Modify the value"),
			myConfig.getConfig()[self.section][self.subsection][theKey], style = wx.TE_MULTILINE | wx.OK | wx.CANCEL)
		if d.ShowModal() == wx.ID_CANCEL:
			return
		newValue = d.Value
		try:
			myConfig.modifyValue(section = self.section, key = theKey, value = newValue, subsection = self.subsection)
		except (KeyError, ValueError):
			gui.messageBox(
			# Translators: An error displayed when the modification fails.
			message = _("Can not modify the value."),
			# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		except:
			log.debugWarning("", exc_info = True)
			gui.messageBox(
			# Translators: An error displayed when the modification fails.
			message = _("Can not modify the value."),
			# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
			return
		self.keysList.Selection = index
		self.keysList.SetFocus()

	def onOpen(self, evt):
		if self.keysList.Selection == wx.NOT_FOUND:
			# Translators: An error displayed when no item is selected in the items list.
			gui.messageBox(
			# Translators: An error message indicating that no selection has been made.
			message = _("No selection found ! Please select an item in the list"),
			# Translators: The caption of the error message.
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
				gui.messageBox(
				# Translators: An error displayed when opening the file or directory fails.
				message = _("Can not open {theItem}, this file or directory does not exist.").format(theItem = myConfig.getConfig()[self.section][self.subsection][item]),
				# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		elif self.section == "myContacts" or self.section == "myNotes":
			theValue = myConfig.getConfig()[self.section][self.subsection][item]
			# We are looking for a contact or a note.
			information = unicode("{theName} {theInfos}", "utf-8").format(theName=item, theInfos=theValue) if sys.version_info.major == 2 else "{theName} {theInfos}".format(theName=item, theInfos=theValue)
			try:
				# We display the information of the selected contact or note in a wx.TextCtrl.
				d = DisplayInformationDialog(parent = self, text = information)
				d.Show()
			except:
				gui.messageBox(
				# Translators: An error displayed when opening the contact's or note information fails.
				message = _("Can not display {theItem}'s information.").format(theItem = item),
				# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		else:
			# We are looking for a journal website or a website.
			try:
				# We open our favorite website or journal website.
				webbrowser.open(myConfig.getConfig()[self.section][self.subsection][item])
			except:
				gui.messageBox(
				# Translators: An error displayed when opening the url website or journal website fails.
				message = _("Can not open the url {theURL}.").format(theURL = myConfig.getConfig()[self.section][self.subsection][item]),
				# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
				return
		# You can comment this line if you prefer to leave the list of items available.
		#self.Destroy()

	def onMoveToGroup(self, evt):
		choices = [key for key in myConfig.getSubsectionsFromSection(section = self.section, exc = self.subsection)]
		choices.sort()
		index = self.keysList.Selection
		item = self.keysList.GetString(index)
		dlg = wx.SingleChoiceDialog(parent = self,
		# Translators: A message asking the user to choose a group to move the element to.
		message = _("Choose the group in {theTopic} topic, where you want to move {element}").format(theTopic = self.Parent.topics[0], element = item),
		# Translators: The title of the dialog asking the user to move the key.
		caption = _ ("Move the element"),
		choices = choices)
		if dlg.ShowModal() == wx.ID_OK:
			if item in myConfig.getConfig()[self.section][dlg.GetStringSelection()].keys():

				gui.messageBox(
				# Translators: An error displayed when the element already exists.
				message = _("This name already exists. Please choose a different name"),
				# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK|wx.ICON_ERROR, parent = self)
				return
			try:
				myConfig.modifyValue(section = self.section, key = item, value = myConfig.getConfig()[self.section][self.subsection][item], subsection = dlg.GetStringSelection())
				myConfig.delItem(section = self.section, key = item, subsection = self.subsection)
			except (KeyError, ValueError):
				gui.messageBox(
				# Translators: An error displayed when the move fails.
				message = _("Can not move {theItem}.").format(theItem = item),
				# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
				return
			except:
				log.debugWarning("", exc_info = True)
				gui.messageBox(
				# Translators: An error displayed when the move fails.
				message = _("Can not move {theItem}.").format(theItem = item),
				# Translators: The caption of the error message.
				caption = _("Error"),
				style = wx.OK | wx.ICON_ERROR, parent = self)
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

class DisplayInformationDialog(wx.Dialog):

	def __init__(self, parent, text):
		super(DisplayInformationDialog, self).__init__(parent = parent,
		# Translators: The title of the dialog to display the selected item information.
		title = _("Information"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(wx.StaticText(self,
		# Translators: The label of the field that should display the information.
		label = _("Information")))
		item = self.contactInformation = wx.TextCtrl(parent = self, value =text, style = wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH, size = (500, 200))
		item.SetBackgroundColour(wx.SystemSettings.GetColour(4))
		sizer.Add(item)
		item.SetFocus()

		item = wx.Button(parent = self, id = wx.ID_CLOSE,
		# Translators: The label of a button to close the dialog.
		label = _("&Close"))
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

