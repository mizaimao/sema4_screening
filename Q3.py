#!/usr/bin/env python3

import sys, os


def colorPrint(str):
	print("\x1b[1;32;44m %s \x1b[0m" %str)


def get_chromosome(file_name):
	# read file
	if file_name.endswith('.gz'):	# just in case a compressed file was input
		direct_out = os.popen('zcat < %s | grep \"^>\"' % file_name).read()	# macOS-compatible syntax, may be different in Linux
	else:
		direct_out = os.popen('grep \"^>\" %s' % file_name).read()

	chr_list = [x[1:] for x in direct_out.split('\n')][:-1]	# list of all chromosomes
	chr_list = chr_list

	# print chromosomes
	colorPrint('Chromosome names appeared in %s' %(file_name))
	print('\n'.join(chr_list))
	return chr_list


if __name__ == "__main__":
	# get two lists of chromosomes from arguments
	if len(sys.argv) < 3:
		print("Usage: ./Q3.py file1.fa.gz hg38.fa")
		exit() 
	fileA = sys.argv[1]; fileB = sys.argv[2]
	setA = get_chromosome(fileA)
	setB = get_chromosome(fileB)

	# two lists are identical, including their orders
	if setA == setB:
		colorPrint("Same chromosomes in %s and %s" %(fileA, fileB))
		exit()

	# otherwise, they are different
	colorPrint("Difference found between %s and %s" %(fileA, fileB))
	# convert them to sets for the convenience of operations
	setA = set(setA); setB = set(setB)
	if setA == setB:	# indicating the only difference is their order
		colorPrint("Chromosome orders are different")
	else:	# otherwise, there are missing components
		intersection = setA & setB
		colorPrint("Missing from %s" %fileA)
		print('\n'.join([str(x) for x in (setB-intersection)]))
		colorPrint("Missing from %s" %fileB)
		print('\n'.join([str(x) for x in (setA-intersection)]))
