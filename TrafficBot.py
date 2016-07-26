# File: traffic_sim.py

#! /usr/bin/env python
import random, pycurl, time, re, datetime
from StringIO import StringIO
from stem import Signal
from stem.control import Controller

url_list = open('var_lists/url_list.txt').read().splitlines()
ref_list = open('var_lists/ref_list.txt').read().splitlines()
ua_list = open('var_lists/ua_list.txt').read().splitlines()
tor_list = open('var_lists/tor_list.txt').read().splitlines()

def new_tor_id(tor_host, tor_control_port, tor_password):
   with Controller.from_port(address = tor_host, port = tor_control_port) as tor_controller:
      tor_controller.authenticate(password = tor_password)
      tor_controller.signal(Signal.NEWNYM)

def write_log_entry(log_entry = "N/A", log_name = "error_log.txt", write_mode = "a"):
   dt = datetime.datetime.now()
   # line_item = str(dt) + " " + log_entry + "\n"
   # line_item = str(dt), " ", log_entry, "\n"
   # line_item = ' '.join(dt, ', ', log_entry, "\n")
   # line_item = ''.join(str(dt), ", ", log_entry, "\n")
   # line_item = ''.join(line_item)
   line_item = ''.join(str(dt) + str(", ") + str(log_entry) + str("\n"))
   # line_item = ' '.join(line_item)

   log = open(log_name, write_mode)
   log.write(line_item)
   log.close

def http_get(http_url, http_ref, http_ua, http_tor, disable_output = True):
   tor_ip, tor_port = http_tor.split(':')

   tor_ip = str(tor_ip)
   tor_port = int(tor_port)

   c = pycurl.Curl()
   c.setopt(c.URL, http_url)
   c.setopt(pycurl.USERAGENT, http_ua)
   c.setopt(pycurl.REFERER, http_ref)
   c.setopt(pycurl.PROXY, tor_ip)
   c.setopt(pycurl.PROXYPORT, tor_port)
   c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
   c.setopt(pycurl.CONNECTTIMEOUT, 3)
   c.setopt(pycurl.TIMEOUT, 3)
   c.setopt(pycurl.FOLLOWLOCATION, 1)

   if disable_output == True:
      c.setopt(pycurl.WRITEFUNCTION, lambda x: None) # no output
   
   c.perform()
   c.close()

def tor_attack(no_of_attack_sessions = 100, attack_wait_from = 10, attack_wait_to = 15):
   current_attack = 1
   attack_session = 1
   attack_failure = 0
   effective_attack = 0

   while attack_session <= no_of_attack_sessions:
      for url_line in url_list:
         current_tor = random.choice(tor_list)

         try:
            http_get(url_line, random.choice(ref_list), random.choice(ua_list), current_tor, True)

            print "Attack Session: ", attack_session
            print "Current Attack: ", current_attack
            print "Attack Failures: ", attack_failure
            # print "Effective Attack: ", effective_attack 
            print "URL: ", url_line
            print "\n"

            current_attack = current_attack + 1

            time.sleep(random.randint(attack_wait_from, attack_wait_to))

         except Exception, e:
            error_log = str("Error: ") + str(current_tor) + str(" ") + str(e)
            
            write_log_entry(error_log)
            print error_log
            # print "Error: ", current_tor, e
            print "\n"

            attack_failure = attack_failure + 1
         
         # tor_ip, tor_port = current_tor.split(':')
         # new_tor_id(tor_ip, 9051)         

      # effective_attack = attack_failure / (attack_failure + current_attack) 
      attack_session = attack_session + 1

tor_attack(100, 1, 2)
