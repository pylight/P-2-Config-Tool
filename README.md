P^2 Config Tool
===============

* Author:    Sven K. (<admin@ganz-sicher.net>)
* Date:      August, 2011
* Version:   0.2
* GitHub:    <https://github.com/pylight/P-2-Config-Tool>
* [German Blogpost](http://ganz-sicher.net/blog/programmierung-scripting/perfect-privacy-tool-fur-den-networkmanager-p2-vpn-config-tool/)
* Dependecies: gksu, networkmanager with a PP-VPN connection (openvpn or pptp), nmcli, python3, python3-gobject

This free software is copyleft licensed under the GPL license.

The goal of this little tool is to make switching between Perfect 
Privacy-Servers (http://perfect-privacy.com/) easier with Networkmanager / 
under Gnome. P^2 Config Tool is developed for Python 3.x, using Glade and Gtk3.


List of Changes:
----------------
[0.2]	Tray Icon added to hide/show tool


Usage:
------

You will need to have an active Perfect Privacy account and you have to 
set up a PP VPN connection in NetworkManager with your login data. The 
tool will help you switch between the different PP-Servers quickly, but 
it doesn't *create* the VPN-Configuration at the moment.

To start the tool, just execute the  pptool.py Script with python from 
the terminal, eg. on Archlinux:

	python3.2 pptool.py
	
On first run, the tool will ask for some settings, so the terminal is 
needed here. You can later start the GUI without an open terminal of course.

You could for example place a bash script in your /usr/bin like this
to run the tool easier:
<pre>
#!/bin/bash

cd /path/folder/with/script
python3.2 pptool.py
</pre>


Important Notes
---------------

Please note that you need to create a **working PP VPN-Connection** 
(see http://goo.gl/D84IG for help) to use this tool.

On first run you are asked to insert the name of the connection. (in the screen below it would be: PP)


Installation under Ubuntu
---------------------------------

Ubuntu 11.04: [see wiki](https://github.com/pylight/P-2-Config-Tool/wiki/Installation-%28Ubuntu-11.04%29)

Ubuntu 11.10 and later:

You'll need python3.2 and python3-gobject:
<pre>sudo apt-get install python3.2 python3-gobject</pre>

Create an PP VPN-Connection (openvpn or pptp) with your username and password, start the tool and follow the configuration process.


Installation under Gnome 3 with Archlinux or Fedora
-----------------------------------------------

Gnome 3 comes with GTK+3 but you'll possibly need (Archlinux):
<pre>pacman -S python python-gobject</pre>

In Fedora it would be:
<pre>yum install python3 python3-gobject</pre>


Screenshots
------------

Gnome3/Archlinux:

![](http://i.imgur.com/fIED5.jpg)

![](http://i.imgur.com/grlZu.jpg)

Ubuntu 11.10:

![](http://i.imgur.com/vlV8x.png)


Issues or Suggestions?
----------------------

This tool is in a very early stage of development so I'm happy about 
every comment, suggest and your ideas! Please feel free to contact me 
here or via E-Mail. =)
