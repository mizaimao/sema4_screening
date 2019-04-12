#!/usr/bin/env python3

from mysqlHelper import connect
import sys
import argparse


def get_gene_name(chr, pos, connection, highlight=False):
	cursor=connection.cursor()
	cursor.execute("""SELECT name FROM ensGene 
						WHERE chrom = ("%s")
						AND txStart <= ("%s") 
						AND txEnd >= ("%s");""" % (chr, pos, pos))
	info = cursor.fetchall()
	if not info:	# empty list, meaning something went wrong
		print("Could not find gene name on chromosome %s at position %s" %(chr, pos), 
			file=sys.stderr)	#	printing to srderr
		exit(1)		# exit with code 1

	if highlight:
		print("\x1b[1;32;44m" + "Result(s) on %s:%s" %(chr, pos) + "\x1b[0m")
	names = [x[0] for x in info]	# otherwise print each record per line
	print('\n'.join(names))

	return


if __name__ == "__main__":
	# arg processing
	parser = argparse.ArgumentParser(description='Show gene name for a given chromosome and position.')
	parser.add_argument('-c', '--chromosome', default=None, type=str,	help='Name of chromosome, for example, chr17')
	parser.add_argument('-p', '--position', default=None, type=str, help='Position on chromosome, for example, 79156766')
	chr = parser.parse_args().chromosome
	pos = parser.parse_args().position

	# create a connection
	connection = connect()	

	# calling function
	if chr and pos:
		get_gene_name(chr, pos, connection, True)
	else:
		parser.print_help()
		print("\n\nBad arguments, showing demo...")
		get_gene_name('chr17', '79156766', connection, True)
		get_gene_name('chr16', '79156766', connection, True)
		get_gene_name('chr17', '79156766', connection, True)
		get_gene_name('chrX', '79156766', connection, True)
	
