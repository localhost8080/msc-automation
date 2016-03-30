#!/usr/bin/env python
import sys
import os
import subprocess
import signal
import re

class jonathans_scanner_authenticator:

	def __init__(self, utility_name, platform_name):	
		# set the current working path (to store a cookie in a temporary file)
		self.pwd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))	
		# blank variables to hold our actual sessiob ID's and cookie files
		self.session_id = ''
		self.cookiefile = ''
		self.jsoncookiefile = ''

		#the platform we are testing
		self.platform_name = platform_name
		
		#auth with platform
		self.cleanup()
		self.authenticate()
		self.set_cookie()
				
	def cleanup(self):
		# we cant cleanup after, due to the way python subprocess forks, so we will do a cleanup of any old files before
		cleanup = subprocess.Popen(os.path.join(self.pwd,'cleanup'), shell=False)
		cleanup.wait()

	def authenticate(self):
		# fork a subprocess and call a bash script that uses wget to request a cookie and keep its session ID
		authenticator = subprocess.Popen(os.path.join(self.pwd, 'authenticate_'+self.platform_name), shell=False)
		authenticator.wait()

	def set_cookie(self):
		# set our class properties that hold our actual cookie information to be used by our individual tools
		self.session_id = ''

		if self.is_non_zero_file(os.path.join(self.pwd,'session.txt'))
			session_content = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'session.txt'))]
			self.session_id = ' '.join(session_content)
		
		# set some class properties to be used with actual cookie files
		self.cookiefile = os.path.join(self.pwd,'cookie.txt')
		self.jsoncookiefile = os.path.join(self.pwd,'cookie.json')

	def is_non_zero_file(fpath):  
    	return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False
		








