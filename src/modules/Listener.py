"""
 (_) ___ _ __ ___  _ __ | |/ / \ | |/ _ \ / ___| |/ /   
 | |/ __| '_ ` _ \| '_ \| ' /|  \| | | | | |   | ' /    
 | | (__| | | | | | |_) | . \| |\  | |_| | |___| . \    
 |_|\___|_| |_| |_| .__/|_|\_\_| \_|\___/ \____|_|\_\   
                  |_| (c) by Victor Dorneanu

icmpKNOCK - ICMP port knocking server
Copyright (C) 2009-2010 by Victor Dorneanu
"""

import socket
import time
import datetime
import sys
import string
import os
from modules.Utils import *

# --- Listen for ICMP packets 
class ICMPListener(object):

    def __init__(self, actions, opts, g_opts):
        """
             Servers constructor
             * Set actions, port knock delay etc.
             * Create socket to listen for ICMP requests
        """

        # Set config options
        self.opts = opts

        # Set global options
        self.g_opts = g_opts

        # Set actions
        self.actions = actions

        # List of key sequences
        self.keys = []

        # Payloads 
        self.payloads = {}
   
        # Fetch keys and create list of key sequences
        for a in actions:
            k = actions[a]['keys']
            t = tuple(k.split(','))
            self.keys.append(t)                            # Append to list of key sequences
            self.payloads[t] = actions[a]['payload']       # Send payload according to key sequence
        

        # Knocking delay time limit
        self.knock_delay = string.atoi(self.opts['knock_delay'])
        self.last_knock = time.time()

        self.pattern_seq = []

        # Open socket (requires roOt)
        # TODO: if id != 0 then exit
        # Debug
        if self.g_opts['debug']:
            Utils.show_debug_msg(Utils.whoami(self), "Creating listening socket (AF_INET, SOCK_RAW, IPPROTO_ICMP)")

        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.sock.bind(('', 1))



    def go(self):
        """ Receive and process a requests """

        # Debug
        if self.g_opts['debug']:
            Utils.show_debug_msg(Utils.whoami(self), "Listening for incomming packets ...")

        while True:
            try:
                data = self.sock.recv(1024)
            except socket.error, e:
                print "Can't receive packet"
                raise
          
            # Debug
            if self.g_opts['debug']:
                Utils.show_debug_msg(Utils.whoami(self), "Packet received! Length: %s" % str(len(data)))

            self.check_packet(self.parse_packet(data))



    def check_packet(self, value):
        """ Check if packet contains our keys """
        
        # Check for knock delay 
        now = time.time()
        
        if now > (self.last_knock + self.knock_delay):
            self.pattern_seq = []

        # Set last knock
        self.last_knock = now

        # Try to find sequence in current packet
        for s in self.keys:
            seq = s

            # Check key in value (pattern)
            for j in seq:
                if (j in value) and not (j in self.pattern_seq):
                    
                    if len(self.pattern_seq) <= self.opts['max_req']:
                        self.pattern_seq.append(j)
                        # Debug
                        if self.g_opts['debug']:
                            Utils.show_debug_msg(Utils.whoami(self), "\n\t Storing seq <%s>" % j)   

            try:
                # Check if current key sequence has action (call payload)
                seq_key = tuple(self.pattern_seq)
            
                # Execute payload
                if self.payloads.has_key(seq_key):

                    # Debug
                    if self.g_opts['debug']:
                        Utils.show_debug_msg(Utils.whoami(self), "Found complete key(s) sequence!")
                        Utils.show_debug_msg(Utils.whoami(self), "Executing: %s" % self.payloads[seq_key])

                    os.system(self.payloads[seq_key])
                   
                    # Flush list of received packets
                    del self.pattern_seq[:]
                    break
                
            except KeyError:
                pass



    def parse_packet(self, data):
        """ Parse packet and return HEX string """

        # Split packet into IP header and data (RFC 791)
        ip_header, ip_data = data[:20], data[20:]

        # Split IP data into ICMP header and ICMP data (RFC 792)
        icmp_header, icmp_payload = ip_data[:8], ip_data[8:]

        # Return payload data as hex string representation
        return ''.join( [ "%02x" % ord( x ) for x in icmp_payload ] ).strip()


