# -*- coding: utf-8 -*-
"""
	database helper
"""
__author__  = """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__    = "2015-08-08"
__version__ = "0.1.0"
__license__ = """MIT"""

import sqlite3
import os
import logging
import yaml

import threading

def dict_factory(cursor, row):
	d = {}
	for idx,col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

class Database():
	def __init__(self,conf):
		pass