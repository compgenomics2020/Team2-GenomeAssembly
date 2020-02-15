#!/usr/bin/env python
import os
import subprocess

def abyss_runner(fastq_file_forward, fastq_file_reverse, input_directory_path, output_directory_path, k_value=21):

	#Create file paths.
	fastq_file_forward_path = input_directory_path + fastq_file_forward
	fastq_file_reverse_path = input_directory_path + fastq_file_reverse

	#Creating a directory inside output directory.
	output_subdir_name = fastq_file_forward.split('.')[0].split('_')[0]
	output_subdir_path = output_directory_path.rstrip('/') + '/' + output_subdir_name 

	#Check if subdir is already there.
	if not output_subdir_name in os.listdir(output_directory_path):
		os.mkdir(output_subdir_path)

	try:
		print("Running ABySS for {} and {}".format(fastq_file_forward, fastq_file_reverse))
		abyss_output = subprocess.check_output(["abyss-pe", "k={}".format(k_value), "name=abyss_result", "in={} {}".format(fastq_file_forward_path, fastq_file_reverse_path), "-C", output_subdir_path])
	except subprocess.CalledProcessError:
		print("ABySS could not finish the assembly. Please check the files.")
		return False

	print("Successfully ran ABySS for {} and {}".format(fastq_file_forward, fastq_file_reverse))
	return True

if __name__ == "__main__":
	#abyss_runner()
	pass
