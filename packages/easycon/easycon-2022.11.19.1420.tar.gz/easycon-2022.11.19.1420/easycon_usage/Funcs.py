#!/usr/bin/env python3

#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# Class:   Funcs
#──────────────────────────
# Author:  Hengyue Li
#──────────────────────────
# Version: 2019/03/01
#──────────────────────────
# discription:
#          operation between local PC with a remote server
#          remember to call connect or disconnect for some function.
#
#──────────────────────────
# Imported :
import os , configparser,json,base64,logging
#──────────────────────────
# Interface:
#
#        [fun] readConfig(path)
#              return a dict used for paramiko
#
#        [sub] mkConfig(path)
#              create a new configuration file.
#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════

class Funcs():



    @classmethod
    def pharseInputConfig(cls,argStr):
        if os.path.exists (argStr):
            logging.debug("config file exists, use it")
            return cls.readConfig(argStr)
        else:
            logging.info("input config is not a file or filepath not exist, try pharse it")
            return json.loads(base64.b64decode(argStr.encode()))


    @staticmethod
    def readConfig(path):
        if os.path.isfile(path):
            config = configparser.ConfigParser()
            config.read(path)
            paramikoCon = dict(config._sections['Server configuration'])
            return paramikoCon
        else:
            return "error: configurate file: {} not exist".format(path)


    @staticmethod
    def mkConfig(path):
        S = """[Server configuration]
# If password is empty, this must be specified.
hostname = 1.1.1.1
username = root
#port =  22
#password  =  FLVFjn17cxpdGEWQ2S
#key_filename = local/path/to/key.pem
        """
        open(path,'w').write(S)
