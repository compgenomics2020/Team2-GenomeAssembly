#!/usr/bin/env python

'''
Welcome to the backbone script of Team-2's Genome Assembly Group.

This script is responsible for calling various functional blocks of
Genome Assembly pipeline.

Input: 	This script takes in Input fastq files. We expect paired-end or single-end libraries.
		Ideally we should generalize more, for mate-pairs and sequencing instrument information and what not.
		But we're focusing on basic functionality right now.

Output:	-	The final output is going to be Genome Assembly contigs for respective read files given. For paired-end libraries,
			one can expect 1 contig file for every file pair.
		-	We're also going to send the organism name to the next group in the main pipeline.
		-	There are also intermediate output that we are generating, we'll be sending them to the web server people
			to display thing if needed.
'''

import argparse
import subprocess

#############################Globals#############################

#Please do not change or add keys in the following dictionary.
#Please do not use direct_paths unless you have to.
genome_assembly_tools = {'in_path_variable': ['spades.py'], 'direct_paths': []}


def check_tools():
	'''
	This function checks if all the tools required for our pipeline to work.
	It uses the 'genome_assembly_tools' global dictionary to see if everything is all right. 
	'''
	for tool_name in genome_assembly_tools['in_path_variable']:
		try:
			bash_output = subprocess.check_output([tool_name])
		except (FileNotFoundError, subprocess.CalledProcessError) as error:
			print("A tool: {}, was not present on the system. Now quitting...".format(tool_name))
			return False




def main():
	parser = argparse.ArgumentParser()

	#Arguments added for an input-directory and output-directory.
	parser.add_argument("-i", "--input-directory", help="Path to a directory that contains input fastq files.", required=True)
	parser.add_argument("-o", "--output-directory", help="Path to a directory that will store the output files.", required=True)	

	#Parsing the arguments.
	args = vars(parser.parse_args())

	input_directory_path_for_fastq_files = args['input_directory']
	output_directory_path = args['output_directory']


	#Check if all the tools are present. Either the tool should be present in the PATH variable 
	#or the bioinformatician should make sure that a proper path to their tool is sent.
	#Pipeline cannot work without tools.
	check_tools_output = check_tools()

	if not check_tools_output:
		return False, "Tools asked for by the Genome Assembly weren't present on the system."




if __name__ == "__main__":
	'''
	For Unit testing the functionality of Genome Assembly group.
	Always make sure that this script is working intact when called specifically.
	'''
	main()


























































