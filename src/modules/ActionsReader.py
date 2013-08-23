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

# Define here which options actions _must_ have
sections = {"action" : ["keys", "payload"]}

class ActionsReader:
    def __init__(self, filepath, opts):
        """
            Read actions file
            and return options
        """
        self.config = ConfigParser.RawConfigParser()
        self.filepath = filepath
        self.opts = opts



    def read_actions(self):
        """ Read config file and check options """
        res = {}

        self.config.read(self.filepath)

        # Check if actions were defined in the configuration file
        for s in self.config.sections():
           
            # Check if action has specified options
            opts = {}
            for o in sections["action"]:
                if self.config.has_option(s, o):
                    opts[o] = self.config.get(s, o)
                    
                    # Debug
                    if self.opts['debug']:
                        Utils.show_debug_msg(Utils.whoami(self), "\tFound action: %s" % s)

            res[s] = opts
                    

        # Return map including actions and options
        return res



    def clean_actions(self, actions):
        """ Clean/sanitize actions options """
        for a in actions:
            # Remove any newline characters in <keys>
            keys = actions[a]['keys']
            keys = keys.replace("\n","")
            actions[a]['keys'] = keys

        return actions

# EOF
