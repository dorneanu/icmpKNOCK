"""
 (_) ___ _ __ ___  _ __ | |/ / \ | |/ _ \ / ___| |/ /   
 | |/ __| '_ ` _ \| '_ \| ' /|  \| | | | | |   | ' /    
 | | (__| | | | | | |_) | . \| |\  | |_| | |___| . \    
 |_|\___|_| |_| |_| .__/|_|\_\_| \_|\___/ \____|_|\_\   
                  |_| (c) by Victor Dorneanu

icmpKNOCK - ICMP port knocking server
Copyright (C) 2009-2010 by Victor Dorneanu
"""

import ConfigParser
from modules.Utils import *

g_section = 'general'

class ConfReader:
    def __init__(self, filepath, opts):
        """
            Read configuration file
            and return options
        """
        self.config = ConfigParser.RawConfigParser()
        self.filepath = filepath
        self.opts = opts



    def read_conf(self):
        """ Read config file and check options """
        res = {}

        self.config.read(self.filepath)

        # Get all options and create map option -> value
        opts = self.config.options(g_section)

        for o in opts:
           res[o] = self.config.get(g_section, o)
           
           # Debug
           if self.opts['debug']:
               Utils.show_debug_msg(Utils.whoami(self), "\tFound option: %s" % o) 

        return res
# EOF
