#!/usr/bin/env python
import sys
import os
import subprocess
import signal
import re
from zapv2 import ZAPv2


class jonathans_scanner:

	def __init__(self, utility_name):	
		self.ultilty_name = utility_name
		self.pwd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))	
		self.reports_path = os.path.join(self.pwd, 'reports')
		self.reports = os.path.join(self.reports_path, self.ultilty_name)
		
		# need these for dvwa and for wordpress
		self.dvwa_cookiefile = os.path.join(self.pwd,'cookie.txt')
		self.dvwa_jsoncookiefile = os.path.join(self.pwd,'cookie.json')
		self.dvwa_urls = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'dvwa-urls.txt'))]


		self.wp15_cookiefile = os.path.join(self.pwd,'wordpress1-5cookie.txt')
		self.wp15_jsoncookiefile = os.path.join(self.pwd,'wordpress1-5cookie.json')
		self.wp15_urls = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'wordpress1-5urls.txt'))]

		self.authenticated = self.authenticate()
		dvwa_session_content = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'session.txt'))]
		wp15_session_content = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'wordpress1-5session.txt'))]
		self.dvwa_session_id = ' '.join(dvwa_session_content)
		self.wp15_session_id = ' '.join(wp15_session_content)
		self.logfile = ''
		self.base_url = ''
		self.fixed_base_url = ''

	def runThread(self, cmd, logfile):
		print >> logfile, "\n"+cmd+"\n\n\n"
		print "\n"+cmd+"\n\n\n"
		thread = subprocess.Popen("exec " + cmd , shell=True, stdout=logfile)
		thread.wait()
	    
	def launchZaproxy(self):
		zap = ZAPv2()

		#cmd = '/usr/share/zaproxy/zap.sh -daemon -dir ' + self.reports + ' -newsession ' + self.ultilty_name
		#zaproxy_instance = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
		#return zaproxy_instance

	def closeZaproxy(self, zaproxy_instance):
		os.killpg(os.getpgid(zaproxy_instance.pid), signal.SIGTERM)
		
	def authenticate(self):
		# we cant cleanup after, due to the way subprocess forks, so we will do a cleanup before
		cleanup = subprocess.Popen(os.path.join(self.pwd,'cleanup'), shell=False)
		cleanup.wait()
		
		authenticate = subprocess.Popen(os.path.join(self.pwd,'authenticate-dvwa'), shell=False)
		authenticate.wait()

		authenticate = subprocess.Popen(os.path.join(self.pwd,'authenticate-wordpress1-5'), shell=False)
		authenticate.wait()		

	def setUrls(self, url):
		self.base_url = url[:url.find('?')]
		self.fixed_base_url = re.sub('[^A-Za-z0-9]+', '_', self.base_url)
		self.logfile = os.path.join(self.reports, self.fixed_base_url + '.txt')

	def begin(self, cmd):
		#cmd = '/usr/share/zaproxy/zap.sh -newsession ' + self.ultilty_name + '.zaproxy'
		#zaproxy_instance = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid) 
		with open(self.logfile, "w") as log:
			print >> log, "Scan results\n"
			self.runThread(cmd, log)
		#os.killpg(os.getpgid(zaproxy_instance.pid), signal.SIGTERM)






