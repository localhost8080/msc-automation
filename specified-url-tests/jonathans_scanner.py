#!/usr/bin/env python
import sys
import os
import subprocess

class jonathans_scanner:

	def __init__(self, utility_name):
		
		self.ultilty_name = utility_name
		self.pwd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))	
		self.reports_path = os.path.join(self.pwd, 'reports')
		self.reports = os.path.join(self.reports_path, self.ultilty_name)
		self.logfile = os.path.join(self.reports, 'report.txt')
		self.cookiefile = os.path.join(self.pwd,'cookie.txt')
		self.jsoncookiefile = os.path.join(self.pwd,'cookie.json')
		self.urls = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'urllist.txt'))]
		self.session_id =  open(os.path.join(self.pwd,'session.txt'))
		self.authenticated = self.authenticate()
		# self.launchZaproxy


	def runThread(self, cmd, logfile):
	    thread = subprocess.Popen(cmd, shell=False, universal_newlines=True, stdout=logfile)
	    thread.wait()
	    return thread

	def logResult(self, scanner, logname):
	    with open(logname, "a") as log:
	        print >> log, "loading scanner: " + scanner
	        print scanner
	        thread = runThread(scanner, log)

	def launchZaproxy(self):
		cmd = 'zaproxy -daemon -newsession ' + self.reports
		thread = subprocess.Popen(cmd, shell=False, universal_newlines=True)
		

	def authenticate(self):
		# we cant cleanup after, due to the way subprocess forks, so we will do a cleanup before
		cleanup = subprocess.Popen(os.path.join(self.pwd,'cleanup'), shell=False)
		cleanup.wait()
		
		authenticate = subprocess.Popen(os.path.join(self.pwd,'authenticate-dvwa'), shell=False)
		authenticate.wait()

	def begin(self, cmd):

		with open(self.logfile, "w") as log:
			print >> log, "Scan results"
			self.runThread(cmd, log)






