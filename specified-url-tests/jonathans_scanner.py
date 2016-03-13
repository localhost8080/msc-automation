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

		#auth with them all for now
		self.authenticate()
		self.set_cookie()
		
		self.logfile = ''
		self.base_url = ''
		self.fixed_base_url = ''

	def runThread(self, cmd, logfile):
		print >> logfile, "\n"+cmd+"\n\n\n"
		print "\n"+cmd+"\n\n\n"
		thread = subprocess.Popen("exec " + cmd , shell=True, stdout=logfile)
		thread.wait()
		
	def authenticate(self):
		# we cant cleanup after, due to the way subprocess forks, so we will do a cleanup before
		cleanup = subprocess.Popen(os.path.join(self.pwd,'cleanup'), shell=False)
		cleanup.wait()
		
		self.run_auth('authenticate_dvwa')
		self.run_auth('authenticate_wp15')
		self.run_auth('authenticate_joomla')

	def run_auth(self, platform):
		authenticate = subprocess.Popen(os.path.join(self.pwd,platform), shell=False)
		authenticate.wait()

	def set_cookie(self):
		dvwa_session_content = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'session.txt'))]
		wp15_session_content = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'wp15_session.txt'))]
		joomla_session_content = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'joomla_session.txt'))]
		self.dvwa_session_id = ' '.join(dvwa_session_content)
		self.wp15_session_id = ' '.join(wp15_session_content)
		self.joomla_session_id = ' '.join(joomla_session_content)

	def set_urls(self):
		# need these for dvwa
		self.dvwa_cookiefile = os.path.join(self.pwd,'cookie.txt')
		self.dvwa_jsoncookiefile = os.path.join(self.pwd,'cookie.json')
		self.dvwa_urls = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'dvwa_urls.txt'))]

		# need these for wordpress
		self.wp15_cookiefile = os.path.join(self.pwd,'wp15_cookie.txt')
		self.wp15_jsoncookiefile = os.path.join(self.pwd,'wp15_cookie.json')
		self.wp15_urls = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'wp15_urls.txt'))]

		# need these for joomla
		self.joomla_cookiefile = os.path.join(self.pwd,'joomla_cookie.txt')
		self.joomla_jsoncookiefile = os.path.join(self.pwd,'joomla_cookie.json')
		self.joomla_urls = [line.rstrip('\n') for line in open(os.path.join(self.pwd,'joomla_urls.txt'))]

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






