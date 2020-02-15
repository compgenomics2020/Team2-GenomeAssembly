#!/usr/bin/env python

import subprocess
import os

def create_configuration_file(fastq_file_forward_path, fastq_file_reverse_path, output_subdir_path, kmer, mean_length, standard_deviation):
	raw_text = "DATA\n" 
	raw_text += "PE= p1 " + str(mean_length) + " " + str(standard_deviation) + " " + fastq_file_forward_path + " " + fastq_file_reverse_path + "\n"
	raw_text += "END\nPARAMETERS\n"
	raw_text += "GRAPH_KMER_SIZE = " + kmer + "\n"
	raw_text += "USE_LINKING_MATES = 1\nMEGA_READS_ONE_PASS=0\nCA_PARAMETERS =  cgwErrorRate=0.25\nCLOSE_GAPS=1\nNUM_THREADS = 8\nJF_SIZE = 200000000\nEND"

	masurca_config_script_path = output_subdir_path.rstrip('/') + '/' + "config.txt" 

	#print(masurca_config_script_path)

	with open(masurca_config_script_path, 'w') as f:
		f.write(raw_text)

	return masurca_config_script_path


def masurca_runner(fastq_file_forward, fastq_file_reverse, input_directory_path, output_directory_path, kmer, mean_length, standard_deviation):
	#Create file paths.
	fastq_file_forward_path = input_directory_path + fastq_file_forward
	fastq_file_reverse_path = input_directory_path + fastq_file_reverse
	
	#print(fastq_file_forward_path, os.path.abspath(fastq_file_forward_path))
	#Creating a directory inside output directory.
	output_subdir_name = fastq_file_forward.split('.')[0].split('_')[0]
	output_subdir_path = output_directory_path.rstrip('/') + '/' + output_subdir_name 

	#Check if subdir is already there.
	if not output_subdir_name in os.listdir(output_directory_path):
		os.mkdir(output_subdir_path)

	#Execute MaSuRCA.
	try:
		print("Running MaSuRCA for {} and {} with mean length: {}, and standard deviation: {}".format(fastq_file_forward, fastq_file_reverse, mean_length, standard_deviation))
		
		#Creating configuration file.
		configuration_file_path = create_configuration_file(os.path.abspath(fastq_file_forward_path), os.path.abspath(fastq_file_reverse_path), output_subdir_path, kmer, mean_length, standard_deviation)
			
		bash_output = subprocess.check_output(["masurca",  configuration_file_path, "-o", output_subdir_path.rstrip('/') + '/' + "assembly.sh"])
		

		#Present working directory.
		pwd = os.getcwd()
		
		#Changing working directory to output.
		os.chdir(output_subdir_path.rstrip('/') + '/')

		#Running assembly.
		masurca_output = subprocess.check_output(["./assembly.sh"])
		#print(os.listdir())
		#Switching the directory back.
		os.chdir(pwd)
		
	except subprocess.CalledProcessError:
		os.chdir(pwd)
		print("MaSuRCA could not finish the assembly. Please check the files.")
		return False

	print("Successfully ran MaSuRCA for {} and {}".format(fastq_file_forward, fastq_file_reverse))
	return True


if __name__ == "__main__":
	#masurca_runner()
	pass


'''
DATA

PE= p1 135 20 /home/projects/group-b/test-output-assembly/masurca/CGT2049_1.fq /home/projects/group-b/test-output-assembly/masurca/CGT2049_2.fq

END

PARAMETERS

GRAPH_KMER_SIZE = auto

USE_LINKING_MATES = 1

MEGA_READS_ONE_PASS=0

CA_PARAMETERS =  cgwErrorRate=0.25

CLOSE_GAPS=1

NUM_THREADS = 16

JF_SIZE = 200000000

END
'''
