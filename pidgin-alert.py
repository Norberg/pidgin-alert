#!/usr/bin/env python
# Copyright 2009 Simon Norberg
import re, random, os
import dbus, gobject
from threading import Timer
from dbus.mainloop.glib import DBusGMainLoop, threads_init
from subprocess import Popen
import writeLED

class PidginSMS:
	def recv_msg(self, account, sender, message, conv, flags):
		if self.is_unseen(conv):
			message = self.strip_html(message)
			print sender, "said:", message
			Popen(["espeak", "-v","sv","-s","100",
			       sender + ": " + message])
	def got_attention(self, account, sender, conv, type):
		print sender, conv, type
		writeLED.sendLED(["red", "100"])

	def conversation_updated(self,conv,type):
		if self.is_unseen(conv):
			writeLED.sendLED(["red", "5"])
		else:
			writeLED.sendLED(["red", "0"])
			
	def strip_html(self, string):
		p = re.compile("<[^<]*?>")
		return p.sub("", string)
	def is_unseen(self, conv):
		k = self.purple.PurpleConversationGetData(conv,"unseen-count")
		if k == 0:
			return False
		else:
			return True

	def __init__(self):
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
		#Signal for CoversationUpdates
		bus.add_signal_receiver(self.conversation_updated,
					dbus_interface=
					"im.pidgin.purple.PurpleInterface",
					signal_name="ConversationUpdated")
		#Signal for incomming messages
		bus.add_signal_receiver(self.recv_msg,
					dbus_interface=
					"im.pidgin.purple.PurpleInterface",
					signal_name="ReceivedImMsg")
	def main(self):
		loop = gobject.MainLoop()
		gobject.threads_init()
		loop.run()

if __name__ == "__main__":
	ps = PidginSMS()
	ps.main()

