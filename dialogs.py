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
	dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.QUESTION, Gtk.ButtonsType.NONE, message)
	
	dialog.add_button("Cancel", Gtk.ResponseType.CLOSE);
	dialog.add_button("OK", Gtk.ResponseType.OK);

	inputField = Gtk.Entry()
	inputField.set_text(defaultInput)
	action_area = dialog.get_content_area()
	action_area.add(inputField)

	dialog.connect("response", dialog_response)

	dialog.show_all()
	dialog.run()
	
	while len(inputField.get_text()) == 0:
			errorDialog("Please enter something. :/")
			dialog.run()
	
	conID = inputField.get_text()
	dialog.destroy()
	
	return conID


# simple dialog with dropdown option field, returns the choices as string
def choiceDialog(message, choices):
	dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.QUESTION, Gtk.ButtonsType.NONE, message)
	
	dialog.add_button("Cancel", Gtk.ResponseType.CLOSE);
	dialog.add_button("OK", Gtk.ResponseType.OK);
	
	# create dropdown box
	box = Gtk.ComboBoxText()
	for item in choices:
		box.append_text(item)
	box.set_active(0)
	
	# add to dialoh
	action_area = dialog.get_content_area()
	action_area.add(box)
	dialog.show_all()
	dialog.run()
	
	# get the choice and return it
	choice = choices[box.get_active()]
	dialog.destroy()
	return choice
