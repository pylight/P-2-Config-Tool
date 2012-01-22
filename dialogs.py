#!/usr/bin/env python
# Filename: dialogs.py

from gi.repository import Gtk
from sys import exit

# handle dialog signals for the config setup
def dialog_response(element, resid):
	if resid == Gtk.ResponseType.CLOSE:
		exit("Error - Setup canceled by user!")
	elif resid == Gtk.ResponseType.OK:
		return

# shows an simple error dialog
def errorDialog(message):
	dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, message)
	dialog.show()
	dialog.run()
	dialog.destroy()

# shows an simple info dialog
def infoDialog(message):
	dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message)
	dialog.show()
	dialog.run()
	dialog.destroy()

# simple input dialog, returns input
def questionDialog(message, defaultInput):
	idDialog = Gtk.MessageDialog(None, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.QUESTION, Gtk.ButtonsType.NONE, message)
	
	idDialog.add_button("Cancel", Gtk.ResponseType.CLOSE);
	idDialog.add_button("OK", Gtk.ResponseType.OK);

	inputField = Gtk.Entry()
	inputField.set_text(defaultInput)
	action_area = idDialog.get_content_area()
	action_area.add(inputField)

	idDialog.connect("response", dialog_response)

	idDialog.show_all()
	idDialog.run()
	
	while len(inputField.get_text()) == 0:
			errorDialog("Please enter something. :/")
			idDialog.run()
	
	conID = inputField.get_text()
	idDialog.destroy()
	
	return conID
