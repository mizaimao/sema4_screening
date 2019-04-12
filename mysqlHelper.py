#!/usr/bin/env python3

from mysql import connector

config = {	# config file for MySQL connection
  'user': 'genome',
  'password': '',
  'host': 'genome-mysql.soe.ucsc.edu',
  'database': 'hg19',
  'raise_on_warnings': True
}


def connect():	# connect to remote database	[helper function for get_gene_info]
	connection = connector.connect(**config)
	print("\x1b[6;30;42m" + "Connected to DB" + "\x1b[0m")
	return connection
