#!/usr/bin/env python

	#############################################################################
	#																			#
	#			P^2 Config Tool for NetworkManager (Gnome)						#
	#		little helper to switch between Perfect Privacy Servers easily!		#	
	#	more infos? please visit https://github.com/pylight/P-2-Config-Tool		#
	#																			#
	#############################################################################

version = "v0.1"
desc = "Little config tool for Perfect Privacy / Gnome Network Manager to change the VPN servers quickly! :)"

import os, sys, configparser, webbrowser
from gi.repository import Gtk, Pango
from urllib.request import urlopen 
from subprocess import Popen

UI_FILE = "gui/window.ui"


def readsettings():
	global mainconfig, confpath
	# try to read tool configuration
	mainconfig = configparser.RawConfigParser()
	confpath = os.path.expanduser("~/.ppvpntool.conf")

	if (os.path.exists(confpath) == False):
		print("\nConfigfile", confpath, "not found. Running Config Setup...")
		print("If you're not sure what your doing, choose the default settings by pressing the enter key!\n") 

		# set configpath
		while True:
			while True:
				mypath = input("Networkmanager Setings Path: [/etc/NetworkManager/system-connections/] ")		
				if (os.path.exists(mypath) == False):
					if(mypath == ""):
						mypath = "/etc/NetworkManager/system-connections/"
						break;
					else:
						print("Invalid / not existing Path!")
				else:
					break
		
			# set connection Name
			connection = input("Enter a name for the VPN conection (Networkmanager/Vpn connection file must exist!): [PP] ")		
			if connection == "":	connection = "PP"

			print("Your configuration is placed in", mypath + connection,"is that correct? [Y/n]", end=" ")
			confirm = input()	
			if confirm == "" or confirm == "y" or confirm == "Y":
				break
			
				print("\nRestarting Setup...")

		# set editor
		myeditor = input("Set (graphical) Editor: [gedit] ")		
		if myeditor == "":	myeditor = "gedit"

		# write config file
		mainconfig.add_section('General')
		mainconfig.set('General', 'path', mypath + connection)
		mainconfig.set('General', 'connection', connection)
		mainconfig.set('General', 'editor', myeditor)

		with open(confpath, 'w') as configfile:
			mainconfig.write(configfile)

	print("Reading configuration...")
	mainconfig.read(confpath)
		

def getvpnsettings():
	vpnconfig = configparser.RawConfigParser()
	vpnconfig.read(mainconfig['General']['path'])
	#gateway = vpnconfig.get("vpn", "gateway")
	# TODO


class VPNTool:
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		# get objects
		self.window = self.builder.get_object('window')
		self.infolabel = self.builder.get_object('menuitem3')
		self.serverlist = self.builder.get_object('serverlist')
			
		self.window.show_all()
		print("Little PP Config Tool " + version + " started!")
		getvpnsettings()
		self.getservers()

	# get the list of avaliable pp-servers from github
	def getservers(self):
		f = urlopen("https://raw.github.com/pylight/P-2-Config-Tool/master/srv/servers.list")
		servers = f.readlines()
		for url in servers:
			self.serverlist.append_text(url.decode("utf-8").rstrip())
		
		self.serverlist.set_active(0)
		f.close()



	""" Menu Items """

	# disconnects the vpn connection if established
	def stop_vpn(self, menuitem):
		print("Disconnecting VPN...")
		pStop = Popen("nmcli con down id " + mainconfig['General']['connection'], shell=True)
		pStop.wait()
		self.infolabel.set_label("VPN Offline")

	# "Edit File"-Menuentrys
	def sysconfig_open(self, menuitem):
		self.open_editor(mainconfig['General']['path'], True)

	def toolconfig_open(self, menuitem):
		self.open_editor(confpath)

	# Open File with editor and check for changes afterwards
	def open_editor(self, filepath, root=False):
		# get "last modified" date
		watcher = os.stat(filepath)
		self.last_modified = watcher.st_mtime
		
		# open the file with an editor
		if root == True:
			pEdit = Popen("gksu " + mainconfig['General']['editor'] + " " + filepath, shell=True)
		else:
			pEdit = Popen(mainconfig['General']['editor'] + " " + filepath, shell=True)
		pEdit.wait()
		
		# was the file changed?
		self.check_changes(filepath)

	# check for file changes
	def check_changes(self, file):
		watcher = os.stat(file)
		this_modified = watcher.st_mtime
		
		# if modified, restart tool to get new settings
		if this_modified > self.last_modified:
			print("File edited - restarting!")
			python = sys.executable
			os.execl(python, python, * sys.argv)

	# open the server status-website with the default browser
	def open_infopage(self, menuitem):
		webbrowser.open("https://www.perfect-privacy.com/members/server.html", new=0)
		
	# show about dialog
	def about_clicked(self, window):
		self.about_dialog = Gtk.AboutDialog()
		self.about_dialog.set_title("About")
		self.about_dialog.set_program_name("PP VPN Tool")
		self.about_dialog.set_version(version)
		self.about_dialog.set_comments(desc)
		self.about_dialog.set_logo_icon_name("applications-internet")
		self.about_dialog.set_website("https://github.com/pylight/P-2-Config-Tool")
		self.about_dialog.connect("response", self.about_close)
		self.about_dialog.show_all()

	# close the about dialog
	def about_close(self, about_dialog, resid):
		self.about_dialog.destroy()

	
	""" Buttons - Server connection (Apply) and Close """
	
	# Apply / (Re)Connect VPN
	def connect_vpn(self, button):
		self.stop_vpn(self)
		print("Connecting to VPN...")
		pCon = Popen("nmcli con up id " + mainconfig['General']['connection'], shell=True)
		stat = pCon.wait()
		if stat == 0:
			self.infolabel.set_label("Connected to VPN")
		else:
			self.infolabel.set_label("Error: Couldn't connect to server!")
		
	# update PP gateway server
	def set_new_server(self, combobox):
		if combobox.get_active() != 0:		
			Popen("gksu " + sys.executable + " srv/set_server.py "+ mainconfig['General']['path'] + " " + self.serverlist.get_active_text(), shell=True)

	# close app
	def destroy(self, window):
		Gtk.main_quit()	



def main():
	readsettings()
	app = VPNTool()
	Gtk.main()

if __name__ == '__main__':
	main()
