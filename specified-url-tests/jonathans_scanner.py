#!/usr/bin/env python
import sys
import os
import subprocess
import signal
import re

class jonathans_scanner:

	def __init__(self, utility_name):	
		self.ultilty_name = utility_name
		self.pwd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))	
		self.reports_path = os.path.join(self.pwd, 'reports')
		self.reports = os.path.join(self.reports_path, self.ultilty_name)
		self.cookiefile = os.path.join(self.pwd,'cookie.txt')
		self.jsoncookiefile = os.path.join(self.pwd,'cookie.json')
		self.urls = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'urllist.txt'))]
		self.authenticated = self.authenticate()
		self.session_id = open(os.path.join(self.pwd,'session.txt'))
		self.logfile = ''
		self.base_url = ''
		self.fixed_base_url = ''

	def runThread(self, cmd, logfile):
	    thread = subprocess.Popen("exec " + cmd, shell=True, universal_newlines=True, stdout=logfile)
	    thread.wait()
	    
	def logResult(self, cmd, logname):
	    with open(logname, "a") as log:
	        print >> log, "loading scanner: " + cmd
	        print cmd
	        thread = runThread(cmd, log)

	def launchZaproxy(self):
		cmd = '/usr/share/zaproxy/zap.sh -daemon -dir ' + self.reports + ' -newsession ' + self.ultilty_name
		zaproxy_instance = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
		return zaproxy_instance

	def closeZaproxy(self, zaproxy_instance):
		os.killpg(os.getpgid(zaproxy_instance.pid), signal.SIGTERM)
		
	def authenticate(self):
		# we cant cleanup after, due to the way subprocess forks, so we will do a cleanup before
		cleanup = subprocess.Popen(os.path.join(self.pwd,'cleanup'), shell=False)
		cleanup.wait()
		
		authenticate = subprocess.Popen(os.path.join(self.pwd,'authenticate-dvwa'), shell=False)
		authenticate.wait()

	def setUrls(self, url):
		self.base_url = url[:url.find('?')]
		self.fixed_base_url = re.sub('[^A-Za-z0-9]+', '_', self.base_url)
		self.logfile = os.path.join(self.reports, self.fixed_base_url + '.txt')

	def begin(self, cmd):
		cmd = '/usr/share/zaproxy/zap.sh -newsession ' + self.ultilty_name + '.zaproxy'
		zaproxy_instance = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid) 
		with open(self.logfile, "w") as log:
			print >> log, "Scan results"
			self.runThread(cmd, log)
		os.killpg(os.getpgid(zaproxy_instance.pid), signal.SIGTERM)






