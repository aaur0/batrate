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
		self.ind.set_attention_icon("new-messages-red")
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

	def check_mail(self):
	    messages, unread = self.gmail_checker('anand.bdk@gmail.com','dell@123')
	    if unread > 0:
	  	  self.ind.set_status(appi.STATUS_ATTENTION)
	    else:
		  self.ind.set_status(appi.STATUS_ACTIVE)
	    return True

	def get_bat_rate(self):
		self.rate= float(commands.getoutput("grep \"^present rate\" /proc/acpi/battery/BAT0/state | awk '{ print $3 }'"))

	def pull_bat_rate(self):
	    self.get_bat_rate()
	    self.ind.set_label(str(self.rate) + "mA");
	    return True
  
	def gmail_checker(self, username, password):
  		i = imaplib.IMAP4_SSL('imap.gmail.com')
	        try:
		    	i.login(username, password)
		        x, y = i.status('INBOX', '(MESSAGES UNSEEN)')
		        messages = int(re.search('MESSAGES\s+(\d+)', y[0]).group(1))
			unseen = int(re.search('UNSEEN\s+(\d+)', y[0]).group(1))
		        return (messages, unseen)
		except:
		        return False, 0

if __name__ == "__main__":
    indicator = BatPower()
    indicator.main()

