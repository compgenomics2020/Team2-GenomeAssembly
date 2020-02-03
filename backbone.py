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
import multiprocessing
import os
import subprocess

from spades_wrapper import spades_runner


#############################Globals#############################

#Please do not change or add keys in the following dictionary.
#Please do not use direct_paths unless you have to.
genome_assembly_tools = {'in_path_variable': ['spades.py'], 'direct_paths': []}
number_of_assembly_tools = 3



def check_tools():
	'''
	This function checks if all the tools required for our pipeline to work.
	It uses the 'genome_assembly_tools' global dictionary to see if everything is all right. 
	'''
	for tool_name in genome_assembly_tools['in_path_variable']:
		try:
			#Calling the tool by name supplied.
			bash_output = subprocess.check_output([tool_name])
		except (FileNotFoundError, subprocess.CalledProcessError) as error:
			print("A tool: {}, was not present on the system. Now quitting...".format(tool_name))
			return False

	for tool_path in genome_assembly_tools['direct_paths']:
		try:
			#Calling the tool by name supplied.
			bash_output = subprocess.check_output([tool_path])
		except (FileNotFoundError, subprocess.CalledProcessError) as error:
			print("A tool with path: {}, was not present on the system. Now quitting...".format(tool_name))
			return False		

	#All is fine.
	return True


def process_input_directory(input_directory_path):
	'''
	Get an idea of what fastq files look like.
	The logic assumes files to be written as: CGT2049_1.fq, CGT2049_2.fq or CGT2049_1.fq.gz, ...
	'''
	#####################Please make sure that all files have a similar naming scheme.#####################

	files = os.listdir(input_directory_path)
	
	#Check if directory is empty.
	if len(files) == 0:
		print("No files present in the directory.")
		return False, "No files present in the directory."

	#Check if at least one fastq file is present.
	fastq_files = [file_name for file_name in files if 'fastq' or 'fq' in file_name.split('.')[-2:]]
	
	#See if they are paired or single. Seperate paired from single as well.
	#This dict looks like: {'CGT2049_1.fq':	'CGT2049_2.fq'}

	fastq_files_dict = {}

	#The for loop below creates the above dict.
	for file_name in fastq_files:
		#Get the prefix name of file.
		file_prefix_name = file_name.split('.')[0].split('_')[0]
		if file_prefix_name in [i.split('.')[0].split('_')[0] for i in list(fastq_files_dict.keys())]:
			for fastq_file_one in list(fastq_files_dict.keys()):
				if fastq_file_one.split('.')[0].split('_')[0] == file_prefix_name:
					fastq_files_dict[fastq_file_one] = file_name
		else:
			fastq_files_dict[file_name] = None

	if None not in (fastq_files_dict.values()):
		#All reads are paired.
		return True, ['paired', fastq_files_dict]

	else:
		#One or more reads are Single-pair.
		return True, ['single', fastq_files_dict]


def run_assemblies(input_directory_path, output_directory_path, fastq_files_dict):
	'''
	We'll call 3 assembly tools, parallely
	'''
	parallel_manager = multiprocessing.Manager()
	status_returned = parallel_manager.dict()

	#Refer: https://stackoverflow.com/questions/10415028/how-can-i-recover-the-return-value-of-a-function-passed-to-multiprocessing-proce
	for fastq_file_forward, fastq_file_reverse in fastq_files_dict.items():
		#Check if foward has an _1 as a suffix.
		if '_1' in fastq_file_forward:
			
			##################SPAdes##################
			#Create directory for SPAdes' results.
			output_spades_path = output_directory_path.rstrip('/') + '/' + 'spades'
			if not os.path.exists(output_spades_path):
				os.mkdir(output_spades_path)

			spades_output = spades_runner(fastq_file_forward, fastq_file_reverse, input_directory_path, output_spades_path) 

			#Check if SPAdes ran fine.
			if spades_output is not True:
				print("SPAdes process failed for reads: {} and {}".format(fastq_file_forward, fastq_file_reverse))

			
			##################Unicycler##################



			##################ABySS##################



			##################Velvet##################




	return True




def main():
	parser = argparse.ArgumentParser()

	#Arguments added for an input-directory and output-directory.
	parser.add_argument("-i", "--input-directory", help="Path to a directory that contains input fastq files.", required=True)
	parser.add_argument("-o", "--output-directory", help="Path to a directory that will store the output files.", required=True)	

	#Parsing the arguments.
	args = vars(parser.parse_args())

	input_directory_path_for_fastq_files = args['input_directory']
	output_directory_path = args['output_directory']

	#Check if directories exist.
	if not os.path.exists(input_directory_path_for_fastq_files) and	not os.path.exists(output_directory_path):
		return False, "Input and Output directories do not exist."

	#Check if all the tools are present. Either the tool should be present in the PATH variable 
	#or the bioinformatician should make sure that a proper path to their tool is sent.
	#Pipeline cannot work without tools.
	status_check_tools = check_tools()

	if not status_check_tools:
		return False, "Tools asked for by the Genome Assembly weren't present on the system."

	#Checks completed. Parse through input directories to see how fastq files are doing.
	status_process_input_directory, return_output_process_input_directory = process_input_directory(input_directory_path_for_fastq_files)

	if not status_process_input_directory:
		return False, return_output_process_input_directory

	fastq_files_dict = return_output_process_input_directory[1]
	
	#################Quality Checks#################
	#Kristine



	#################Passing data over to Genome Assembly Tools#################
	status_run_assemblies = run_assemblies(input_directory_path_for_fastq_files, output_directory_path, fastq_files_dict)



	#################Post Assembly Quality Check#################
	#Quast


	

if __name__ == "__main__":
	'''
	For Unit testing the functionality of Genome Assembly group.
	Always make sure that this script is working intact when called specifically.
	'''
	status = main()
	print(status)

