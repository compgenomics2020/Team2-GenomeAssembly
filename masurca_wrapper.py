#!/usr/bin/env python

import subprocess
import os

def create_configuration_file(fastq_file_forward_path, fastq_file_reverse_path, output_subdir_path, kmer):
	read_length_mean = 0
	read_length_sd = 0
	raw_text = "Data\n" 
	raw_text += "PE= p1 " + str(read_length_mean) + " " + str(read_length_sd) + " " + fastq_file_forward_path + " " + fastq_file_reverse_path + "\n"
	raw_text += "END\nPARAMENTERS\n"
	raw_text += "GRAPH_KMER_SIZE = " + kmer + "\n"
	raw_text += "USE_LINKING_MATES = 1\nMEGA_READS_ONE_PASS=0\nCA_PARAMETERS =  cgwErrorRate=0.25\nCLOSE_GAPS=1\nNUM_THREADS = 16\nJF_SIZE = 200000000\nEND"

	masurca_config_script_path = output_subdir_path.rstrip('/') + '/' + "config.txt" 

	#print(masurca_config_script_path)

	with open(masurca_config_script_path, 'w') as f:
		f.write(raw_text)

	return masurca_config_script_path


def masurca_runner(fastq_file_forward, fastq_file_reverse, input_directory_path, output_directory_path, kmer):
	#Create file paths.
	fastq_file_forward_path = input_directory_path + fastq_file_forward
	fastq_file_reverse_path = input_directory_path + fastq_file_reverse

	#Creating a directory inside output directory.
	output_subdir_name = fastq_file_forward.split('.')[0].split('_')[0]
	output_subdir_path = output_directory_path.rstrip('/') + '/' + output_subdir_name 

	#Check if subdir is already there.
	if not output_subdir_name in os.listdir(output_directory_path):
		os.mkdir(output_subdir_path)

	#Execute MaSuRCA.
	try:
		print("Running MaSuRCA for {} and {}".format(fastq_file_forward, fastq_file_reverse))
		
		#Creating configuration file.
		configuration_file_path = create_configuration_file(fastq_file_forward_path, fastq_file_reverse_path, output_subdir_path, kmer)
		return	
		bash_output = subprocess.check_output(["masurca",  configuration_file_path, "-o", output_subdir_path.rstrip('/') + '/' + "assembly.sh"])
	
		masurca_output = subprocess.check_output(["./assembly.sh"])
	except subprocess.CalledProcessError:
		print("MaSuRCA could not finish the assembly. Please chek the files.")
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
