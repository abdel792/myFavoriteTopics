# My favorite topics #
# Version 21.01 #

* Authors: Abderrahim, Abdellah, Abdelkrim.
* download [stable version](https://github.com/abdel792/myFavoriteTopics/releases/download/v21.01/myFavoriteTopics-21.01.nvda-addon)
* download [development version](https://github.com/abdel792/myFavoriteTopics/releases/download/v21.01-dev/myFavoriteTopics-21.01-dev.nvda-addon)

This add-on allows you to display and consult your favorite topics.

It adds an item in the NVDA Tools menu named "My favorite topics", to open a dialog composed of 6 buttons:

* A "Search on Google or Youtube" button so you can search with Google or Youtube;
* A "Display my favorite websites" button to display the list of your favorite websites;
* A "Display my favorite applications" button to display the list of your favorite applications or directories on your PC;
* A "Display my favorite contacts" button to display the list of your favorite contacts;
* A "Display my favorite journal websites" button to display the list of your favorite journal websites;
* A "Display my notes" button to display the list of your saved notes;
* A "Close" button to close the dialog

## Notes ##

* You can close this dialog just by pressing Escape....).
* You can assign a shortcut to open the dialog in "Input gestures" menu and, more precisely, in the "Tools" category.

## To navigate through the topic lists ##

When you press the button corresponding to a topic, this should open up a dialog box consisting of:

* A list of items from which you can navigate with the vertical arrows;
* An "Open" button, that should allow you to access the selected item in the list;
* An "Add a new group" button, which should allow you to add a new group in the list;
* An "Add a new element" button", which should allow you to add a new element in the list;
* A "Rename the group" button, which should allow you to rename the selected group in the list. (This item appears only if the selected item is a group;
* A "Rename the element" button, which should allow you to rename the selected element in the list.
* A "Modify value" button, which should allow you to change the element value corresponding to the selected item in the liste.
* A "Move to group" button, which should allow you to move the selected element in the list to a group.
* A "Search" button, for searching a contact or note. (available only in the contacts and notes topics);
* A "Delete" button, which should allow you to delete the selected item in the list. If the item is a group, all the contents of this group will be deleted.;
* A "Close" button, which should allow you to close the dialog.

## Notes ##

* You can press the escape button to close each dialog box, and return to the dialog with access to the lists buttons.
* When navigating through the list of items, if you are on a group, its name should be suffixed by the word (Group).
* If you open a group, you should land in the list of keys contained in this group.

* You can assign a keyboard shortcut to open each of the dialog boxes mentioned in previous chapters, in the menu "Input gestures" and, more specifically, in the category 'Tools'.
* When no item is present in the list, only the "Add a new group", "Add a new element" and "Close" buttons are displayed.

## Change for 21.01 ##

* Changed the version numbering of the add-on, citing the year and month.
* Added a topic to save notes;
* Added the ability to do a search on Google or Youtube;
* Added the ability to search contacts or notes.

## Change for 3.0 ##

* Added the compatibility with versions of NVDA using Python 3.

## Changes for 2.0 ##

* Fixed a bug that occurred after closing the Favorite Topics dialog box and preventing it from reopening without relaunching NVDA.

## Change for 1.2 ##

* This version provides the compatibility of the add-on with WxPython version 4, especially for dialog boxes for modifying and renaming keys for each topic;

## Change for 1.1 ##

* This version adds the ability to create and manage sub-groups.
* In the "Display my favorite contacts" topic, the contact's informations are displayed in a text control, to facilitate copying.
* Now, under "My favorite contacts", the values entered for each contact are multiline.

## Changes for 1.0 ##

* Initial version.
