#!/usr/bin/env python

import subprocess
import os

def get_files_by_tools(output_directory_path):
	#Returns a dictionary with contig files based on tools.
	masurca_results = []
	spades_results_untrimmed = []
	spades_results_on_trimmed = []
	skesa_results = []
	abyss_results = []
	velvet_results = []
	unicycler_results = []
	
	for root, dirs, files in os.walk(output_directory_path, topdown=True):
		for name in files:
			if name == "genome.ctg.fasta" or name == "contigs.fasta" or name == "contigs.fa" or name == "assembly.fasta":
				path = os.path.join(root, name)
				
				if "masurca" in path:
					if "9-terminator" in path:
						masurca_results.append(path)	
				
				if "spades" in path:
					if "untrimmed" in path:
						spades_results_untrimmed.append(path)
					if "on_trimmed" in path:
						spades_results_on_trimmed.append(path)
				
				if "skesa" in path:
					skesa_results.append(path)		
				
				if "abyss" in path:
					pass
				
				if "velvet" in path:
					velvet_results.append(path)		
				
				if "unicycler" in path:
					unicycler_results.append(path)


	return {"masurca": masurca_results, "spades_untrimmed": spades_results_untrimmed, 
			"spades_trimmed": spades_results_on_trimmed, "skesa": skesa_results, 
			"abyss": abyss_results, "velvet": velvet_results, "unicycler": unicycler_results}

def quast_runner(output_directory_path):
	#Get output files by tools used.
	all_output_files = get_files_by_tools(output_directory_path)
	
	#############################Directory Prechecks#######################
	quast_output_path = output_directory_path.rstrip('/') + '/' + "quast"

	#First check if quast directory is there.
	if "quast" not in os.listdir(output_directory_path):
		os.mkdir(quast_output_path)

	#Paths for output dirs.
	output_dir_paths = {tool: quast_output_path + '/' + tool for tool in list(all_output_files.keys())}

	#Check if quast directory in output directory has tool directories already.
	for output_dir_path in list(output_dir_paths.values()):
		if not os.path.exists(output_dir_path):
			os.mkdir(output_dir_path)

	for tool_name, files in all_output_files.items():
		for file in files:
			#Get directory path for quast file outputs.
			path_els = file.split('/')
			path_els = path_els[::-1][1:]
			file_path_for_quast = ""
			for path_el in path_els:
				if path_el == tool_name:
					break
				file_path_for_quast = path_el + "-" + file_path_for_quast

			print(file_path_for_quast)

			#######################################################################
			#############################Execute Quast#############################
			try:
				#quast_output = subprocess.check_output([])
				pass
			except subprocess.CalledProcessError:
				print("==========>Quast could not finish quality check for tool: {} & file: {}".format(tool_name, file))
				continue



if __name__ == "__main__":
	pass



