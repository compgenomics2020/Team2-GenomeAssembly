#!/usr/bin/env python

import subprocess
import os

def quast_runner(output_directory_path):
	masurca_results = []
	spades_results_untrimmed = []
	spades_results_on_trimmed = []
	skesa_results = []
	
	for root, dirs, files in os.walk(output_directory_path, topdown=True):
		for name in files:
			if name == "genome.ctg.fasta" or name == "contigs.fasta":
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
	

	print(masurca_results)
	



if __name__ == "__main__":
	pass
