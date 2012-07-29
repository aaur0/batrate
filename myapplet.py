#! /usr/bin/env python
try:
	import appindicator as appi
except Exception,e:
	print "library not present"
import gtk
import sys,imaplib
import commands,gobject
PING_FREQUENCY = 1000

class BatPower:
	def __init__(self):
		''' batpower constrcutor'''
		self.ind = appi.Indicator("battery-power-indicator","battery",appi.CATEGORY_APPLICATION_STATUS)
		self.ind.set_status(appi.STATUS_ACTIVE)
		self.ind.set_attention_icon("battery-red")
		self.menu_setup()
		self.ind.set_menu(self.menu)	


	def menu_setup(self):
		self.menu = gtk.Menu()
		self.quit_item = gtk.MenuItem("Quit")
		self.quit_item.connect("activate", self.quit)
		self.quit_item.show()
		self.menu.append(self.quit_item)

	
	def main(self):
   	 gobject.timeout_add(PING_FREQUENCY , self.pull_bat_rate)
	 gtk.main()    	 


	def quit(self, widget):
	    sys.exit(0)

	def get_bat_rate(self):
		self.rate= float(commands.getoutput("grep \"^present rate\" /proc/acpi/battery/BAT0/state | awk '{ print $3 }'"))

	def pull_bat_rate(self):
	    self.get_bat_rate()
	    self.ind.set_label(str(self.rate) + "mA");
	    return True

if __name__ == "__main__":
    indicator = BatPower()
    indicator.main()

