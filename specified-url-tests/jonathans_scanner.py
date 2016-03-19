#!/usr/bin/env python
import sys
import os
import subprocess
import signal
import re
from jonathans_scanner_authenticator import jonathans_scanner_authenticator

class jonathans_scanner:

	def __init__(self, tool_name, platform_name):	
		# set our tool name
		self.tool_name = tool_name
		self.platform_name = platform_name

		#set misc paths
		self.pwd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))	
		self.reports_path = os.path.join(self.pwd, 'reports')
		self.reports = os.path.join(self.reports_path, self.tool_name)

		#set the list of urls to scan
		self.set_url_list()

		#authenticate
		authenticator = jonathans_scanner_authenticator(tool_name, platform_name)
		#class properties form authenticaor with authenticated session information
		self.session_id = authenticator.session_id
		self.cookiefile = authenticator.cookiefile
		self.jsoncookiefile = authenticator.jsoncookiefile

		#class properties for misc paths and urls
		self.logfile = ''
		self.base_url = ''
		self.fixed_base_url = ''

	def set_url_list(self):
		# set the url list
		self.urls = [line.rstrip('\n') for line in open(os.path.join(self.pwd, self.platform_name+'_urls.txt'))]

	def set_misc_paths(self, url):
		self.base_url = url[:url.find('?')]
		self.fixed_base_url = re.sub('[^A-Za-z0-9]+', '_', self.base_url)
		self.logfile = os.path.join(self.reports, self.fixed_base_url + '.txt')
	
	def launch_tool(self, cmd, logfile):
		# add the actual command sent to the individual tool to its log file
		print >> logfile, "\n"+cmd+"\n\n\n"
		# and send it to the std output (console screen)
		print "\n"+cmd+"\n\n\n"
		# fork a subprocess that runs the actual command and wait till it finishes
		thread = subprocess.Popen("exec " + cmd , shell=True, stdout=logfile)
		thread.wait()
	
	def begin(self, cmd):
		#open the log file so that all output can be kept
		with open(self.logfile, "w") as log:
			#with the log file open, run our tool
			print >> log, "Scan results\n"
			self.launch_tool(cmd, log)






