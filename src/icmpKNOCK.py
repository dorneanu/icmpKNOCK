#!/usr/bin/env python
"""
 (_) ___ _ __ ___  _ __ | |/ / \ | |/ _ \ / ___| |/ /   
 | |/ __| '_ ` _ \| '_ \| ' /|  \| | | | | |   | ' /    
 | | (__| | | | | | |_) | . \| |\  | |_| | |___| . \    
 |_|\___|_| |_| |_| .__/|_|\_\_| \_|\___/ \____|_|\_\   
                  |_| (c) by Victor Dorneanu

icmpKNOCK - ICMP port knocking server
Copyright (C) 2009-2010 by Victor Dorneanu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import socket
import time
import datetime
import sys
import os
import getopt
from modules import Listener
from modules.ActionsReader import *
from modules.ConfReader import *
from modules.Utils import *

# Default configuration file
config_file = "conf/icmpKNOCK.conf"

# Default actions file
actions_file = "conf/actions.conf"

# Global options
g_options = { 'daemon'  : True,
              'debug'   : False, 
              'config'  : config_file,
              'actions' : actions_file
            }


# --- Main procedure
if __name__ == '__main__':
   
    # Print usage menu
    def usage():
        banner = "                                             \
        \n(_) ___ _ __ ___  _ __ | |/ / \ | |/ _ \ / ___| |/ / \
        \n| |/ __| '_ ` _ \| '_ \| ' /|  \| | | | | |   | ' /  \
        \n| | (__| | | | | | |_) | . \| |\  | |_| | |___| . \  \
        \n|_|\___|_| |_| |_| .__/|_|\_\_| \_|\___/ \____|_|\_\ \
        \n                 |_|     v0.2 (c) by Victor Dorneanu \
        \n                                                     \
        \nUsage:                                               \
        \n          -h  Show this help                         \
        \n          -d  Enable debug messages                  \
        \n          -f  Don't daemonize process                \
        \n          -c  Specify general config file            \
        \n              Default: %s                            \
        \n                                                     \
        \n          -a  Specify actions file (see README)      \
        \n              Default %s                             \
        \n                                                     \
        " % (config_file, actions_file)

        print banner

    try:
        
        # Get command line arguments
        opts, args = getopt.getopt(sys.argv[1:], "dfhvc:a:", ["help"])
       
        
        for o, a in opts:
            if o in ("-h", "--help"):        
                usage()
                sys.exit(1)

            elif o == "-f":
                g_options['daemon'] = False

            elif o == "-d":                  
                g_options['debug'] = True
    
            elif o == "-c":
                g_options['config'] = a
                
            elif o == "-a":
                g_options['actions'] = a

            else:                            
                pass

        # Read config file
        if g_options['debug']:
            Utils.show_debug_msg(Utils.whoami(), "Reading conf file %s" % g_options['config'])

        conf = ConfReader(g_options['config'], g_options)
        conf_opts = conf.read_conf()

        # Read actions file
        if g_options['debug']:
            Utils.show_debug_msg(Utils.whoami(), "Reading actions file %s" % g_options['actions'])

        acts = ActionsReader(g_options['actions'], g_options)
        actions = acts.clean_actions(acts.read_actions())
      
        # Daemonize process
        if g_options['daemon']:
            
            # Debug
            if g_options['debug']:
                Utils.show_debug_msg(Utils.whoami(), "Create new child process and become a daemon")

            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(1)


        # Activate ICMP listener
        listener = Listener.ICMPListener(actions, conf_opts, g_options)
        listener.go()

    except getopt.GetoptError, e:
        usage()
        print str(e)
        sys.exit(1)

    except OSError, e: 
        print >>sys.stderr, "fork failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1)

    except KeyboardInterrupt:
        exit('Aborting...')

# EOF
