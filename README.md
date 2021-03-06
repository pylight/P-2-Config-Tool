P² Config Tool
===============
This little tool makes switching between [Perfect Privacy](http://www.perfect-privacy.com)-Servers with NetworkManager VPN-Connections (pptp or openvpn) easier! 
If you don't know how to download Projects from github, take a look at the [First steps](https://github.com/pylight/P-2-Config-Tool/wiki/First-Steps) wiki page. The general installation process can be found below.

* *Author*:    Sven K. (<admin@ganz-sicher.net>)
* *GitHub*:    <https://github.com/pylight/P-2-Config-Tool>
* *License*: [see LICENCE](https://github.com/pylight/P-2-Config-Tool/blob/master/LICENSE)
* *Changelog*: see [CHANGELOG](https://github.com/pylight/P-2-Config-Tool/blob/master/CHANGELOG)
* *Dependecies*: gksu, networkmanager with a PP-VPN connection (openvpn or pptp), nmcli, python3, python3-gobject
* *Screens*: [see Wiki](https://github.com/pylight/P-2-Config-Tool/wiki/Screenshots)
* *Moar*: [German Blogpost](http://ganz-sicher.net/blog/programmierung-scripting/perfect-privacy-tool-fur-den-networkmanager-p2-vpn-config-tool/), [PP Forum Support-Thread](https://forum.perfect-privacy.com/showthread.php?t=2957)

Installation under Ubuntu
---------------------------------

*Ubuntu 11.10 and later*:

You'll need python3.2 and python3-gobject:
<pre>sudo apt-get install python3.2 python3-gobject</pre>

Create an PP VPN-Connection (openvpn or pptp) with your username and password, start the tool and follow the configuration process.

*Ubuntu 11.04*: [see wiki](https://github.com/pylight/P-2-Config-Tool/wiki/Installation-%28Ubuntu-11.04%29)

Installation under Gnome 3 with Archlinux or Fedora
-----------------------------------------------

Gnome 3 comes with GTK+3 but you'll possibly need (Archlinux):
<pre>pacman -S python python-gobject</pre>

In Fedora it would be:
<pre>yum install python3 python3-gobject</pre>


Usage:
------

You will need to have an active Perfect Privacy account and you have to 
set up a PP VPN connection in NetworkManager (pptp and openvpn-connections 
are supported) with your login data. The 
tool will help you switch between the different PP-Servers quickly, but 
it doesn't *create* the VPN-Configuration at the moment.

Get the files with git and go to the project folder:
	
	git clone git://github.com/pylight/P-2-Config-Tool.git
	cd P-2-Config-Tool

To start the tool, just execute the  pptool.py Script with python from 
the terminal, eg. on Archlinux:

	python3.2 pptool.py
	

Configuration:
-------------

Please note that you need to create a **working PP VPN-Connection** 
(see http://goo.gl/D84IG for help) before you use this tool.

On first run, the tool will ask for some settings, so the terminal is 
needed here. You can later start the GUI without an open terminal of course.

You could for example place a bash script in your /usr/bin like this
to run the tool easier:
<pre>
#!/bin/bash

cd /path/folder/with/script
python3.2 pptool.py
</pre>


Issues or Suggestions?
----------------------

This tool is in a very early stage of development so I'm happy about 
every comment, suggest and your ideas! If you've problems using this tool,
please create an [issue](https://github.com/pylight/P-2-Config-Tool/issues/new).
