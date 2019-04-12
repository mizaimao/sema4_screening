#!/usr/bin/env python3

from mysqlHelper import connect
import sys


def merge_intervals(coords):	# merge overlapping exon coordinates	[helper function for get_gene_info]
	merged = []
	coords = sorted(coords, key = lambda x: x[0])	# sort by start pos
	for coord in coords:	# coord[0] is the start of an exon, and coord[1] is the end of an exon
		if not merged or merged[-1][1] < coord[0]:
			merged.append(coord)
		else:
			merged[-1][1] = max(merged[-1][1], coord[1])
	return merged


def get_gene_info(gene_name, connection, file_name=''):	# get info by gene name, and return merged exon coordinates
	# retrive info
	cursor=connection.cursor()
	cursor.execute("""SELECT chrom, exonStarts, exonEnds FROM ensGene AS info 
							INNER JOIN ensemblToGeneName AS nameTable 
							ON nameTable.name = info.name 
							WHERE nameTable.value = ("%s");""" % (gene_name))
	info = cursor.fetchall()

	# process info
	dic = {}	# dictionary, key is chromosome, value is a list of exons coords
	for entry in info:
		chromosome, starts, ends = entry
		starts = starts.split(','); ends = ends.split(',')	# str to list
		assert len(starts) == len(ends)	# number of starts should be the same of ends

		if chromosome not in dic: dic[chromosome] = []	# add key if not existed

		for start, end in zip(starts[:-1], ends[:-1]):	# the last pair will be empty as a result of mysql return format, so ignore them
			dic[chromosome].append([int(start), int(end)])

	if not dic:	
		print('Bad gene name %s' % gene_name, file=sys.stderr)
		return 

	print("\x1b[1;32;44m" + "Result of %s" % gene_name + "\x1b[0m")
	first_line = True
	with open(file_name if file_name else gene_name + '.bed', 'w') as out:	# write to file, default name is gene name
		# I'm not sure if there should be an explicit header at the beginning of the file. 
		# If yes, it should be written here such as:
		#out.write("track name=\"aaa\" description=\"bbb\"\n")
		for chromosome, coords in dic.items():
			chr_counter = 1
			for merged_interval in merge_intervals(coords):
				line = '{}\t{}\t{}\t{}.{}'.format(chromosome, merged_interval[0], merged_interval[1], chromosome, chr_counter)
				out.write(('\n' if not first_line else '') + line)	# to avoid last line as an empty line
				print(line)
				chr_counter += 1; first_line = False

	return 


if __name__ == "__main__":
	connection = connect()
	if len(sys.argv) == 1:
		print("Usage: ./Q1.py gene1 gene2 gene3 ...\nShowing demo on AATK-AS1 and PNRC2\n\n")
		get_gene_info("AATK-AS1", connection)
		get_gene_info("PNRC2", connection)
	else:
		for gene in sys.argv[1:]:
			get_gene_info(gene, connection)
	
	
	
""" Appendix: table columes
['bin', 'name', 'chrom', 'strand', 'txStart', 'txEnd', 'cdsStart', 'cdsEnd', 'exonCount', 'exonStarts', 'exonEnds', 'score', 'name2', 'cdsStartStat', 'cdsEndStat', 'exonFrames']
['name', 'value']
"""