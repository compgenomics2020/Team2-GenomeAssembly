#!/usr/bin/env python

import subprocess
import os

def quast_runner(output_directory_path):
	for root, dirs, files in os.walk(output_directory_path, topdown=True):
		for name in files:
			if name == "final.genome.scf.fasta":
				print(os.path.join(root, name))


if __name__ == "__main__":
	pass
