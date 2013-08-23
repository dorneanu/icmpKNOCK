"""
 (_) ___ _ __ ___  _ __ | |/ / \ | |/ _ \ / ___| |/ /   
 | |/ __| '_ ` _ \| '_ \| ' /|  \| | | | | |   | ' /    
 | | (__| | | | | | |_) | . \| |\  | |_| | |___| . \    
 |_|\___|_| |_| |_| .__/|_|\_\_| \_|\___/ \____|_|\_\   
                  |_| (c) by Victor Dorneanu

icmpKNOCK - ICMP port knocking server
Copyright (C) 2009-2010 by Victor Dorneanu
"""

class Utils:
    """ Provide several utilities like debug messages etc. """
    def __init__(self):
        pass

    @staticmethod
    def show_debug_msg(where, msg):
        """ Print debug message <msg> to the standard output """
        print ">> [%s] %s " % (where, msg)

    @staticmethod
    def whoami(object=""):
        import sys
        if object:
            return Utils.class_name(object) + " :: " + sys._getframe(1).f_code.co_name
        else:
            return sys._getframe(1).f_code.co_name

    @staticmethod
    def class_name(object):
        return object.__class__.__name__


# EOF
