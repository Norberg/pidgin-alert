#!/usr/bin/env python
# Copyright 2009 Simon Norberg
import re, random, os
import dbus, gobject
from threading import Timer
from dbus.mainloop.glib import DBusGMainLoop, threads_init
import writeLED

class PidginSMS:
	def got_attention(self, account, sender, conv, type):
		print sender, conv, type
		writeLED.sendLED(["red", "100"])

	def conversation_updated(self,conv,type):
		k = self.purple.PurpleConversationGetData(conv,"unseen-count")
		if k == 0:
			writeLED.sendLED(["red", "0"])
		else:
			writeLED.sendLED(["red", "5"])
			
	def send_sms(self, message):
		print "Sending SMS... from:",message[0],"containing:",message[1]


	def strip_html(self, string):
		p = re.compile("<[^<]*?>")
		return p.sub("", string)

	def __init__(self):
		self.Convs = {}
		self.messages = {}
		self.t = None
		self.askingForSMS = False
		threads_init()
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		threads_init()
		bus = dbus.SessionBus()
		
		obj = bus.get_object("im.pidgin.purple.PurpleService",
		                     "/im/pidgin/purple/PurpleObject")
		#object used for send messages and more
		self.purple = dbus.Interface(obj,
		                             "im.pidgin.purple.PurpleInterface")
		
		#Signal for nudges
		bus.add_signal_receiver(self.got_attention,
					dbus_interface=
					"im.pidgin.purple.PurpleInterface",
					signal_name="GotAttention")
		#Signal for change
		bus.add_signal_receiver(self.conversation_updated,
					dbus_interface=
					"im.pidgin.purple.PurpleInterface",
					signal_name="ConversationUpdated")
	def main(self):
		loop = gobject.MainLoop()
		gobject.threads_init()
		loop.run()

if __name__ == "__main__":
	ps = PidginSMS()
	ps.main()

