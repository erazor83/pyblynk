#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2015-08-08"
__version__	= "0.1.0"
__license__ = "MIT"

import os
import getopt
import sys
import pwd
import grp

sys.path.append(
	os.path.join(
		os.path.dirname(__file__),
		'inc'
	)
)
sys.path.append(
	os.path.join(
		os.path.dirname(__file__),
		'..'
	)
)
	
"""parse arguments"""
import argparse
parser = argparse.ArgumentParser(
	description='blynkD - Blynk (http://blynk.cc) service written in python'
)
parser.add_argument(
	'-c','--config', type=str, 
	help='configuration file if not given it tries to find files in this order: '+
	'~/.config/blynkd.conf /etc/blynkd.conf ./default.conf'
)
parser.add_argument(
	'-v','--version', action='version', version='%(prog)s '+__version__
)
parser.add_argument(
	'-l','--logger', type=str,default='default',
	help='use a specific logger (has to be configured in config)'
)
parser.add_argument(
	'-u','--user', type=str, default=None,
	help='setuid to user'
)
parser.add_argument(
	'-g','--group', type=str, default=None,
	help='setgid to group'
)
parser.add_argument(
	'-d','--dump-config', action='store_true',
	help='test and dump config'
)

args = parser.parse_args()

"""read configs"""
import yaml

cDir=os.path.dirname(__file__)
cfg_file_list=[
	os.path.join(cDir,'default.conf'),
	'/etc/blynkd.conf',
	os.path.expanduser('~/.config/blynkd.conf')
]
config={}
for cFile in cfg_file_list:
	try:
		config.update(
			yaml.load(open(cFile))
		)
		
	except Exception:
		pass

if args.dump_config:
	import pprint
	pp=pprint.PrettyPrinter()
	pp.pprint(config)
	sys.exit(0)

"""setup logger"""
import logging
import logging.config


if 'logging' in config:
	logging.config.dictConfig(config['logging'])

	if args.logger in config['logging']['loggers']:
		logging.getLogger(args.logger)
	else:
		logging.warning('Logger "%s" not configured' % args.logger)

"""user/group change"""
if args.group != None:
	logging.info("Changing to group %s:%i"%(args.group,grp.getgrnam(args.group).gr_gid))
	os.setgid(grp.getgrnam(args.group).gr_gid)

if args.user != None:
	logging.info("Changing to user %s:%i"%(args.user,pwd.getpwnam(args.user).pw_uid))
	os.setuid(pwd.getpwnam(args.user).pw_uid)

"""main part"""
import database
import lib.server as blynk_server
cServer=blynk_server.createFromConf(
	config['server'],
	database.createFromConf(config['database'])
)

try:
	cServer.run()

except KeyboardInterrupt:
	pass

cServer.stop()

