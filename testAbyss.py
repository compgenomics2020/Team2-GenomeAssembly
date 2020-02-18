#!/usr/bin/env python
import os
import subprocess


def abyss_runner(forward_file, reverse_file, input_directory_path, output_directory_path, k_value):

        fo = input_directory_path + "/" + str(forward_file[i])
        re = input_directory_path + "/" + str(reverse_file[i])

        #Creating a directory inside output directory.
        output_subdir_name = str(forward_file[i]).split('o')[0].split('_')[0]
        output_subdir_path = output_directory_path.rstrip('/') + '/' + output_subdir_name 

        #Check if subdir is already there.
        if not output_subdir_name in os.listdir(output_directory_path):
                os.mkdir(output_subdir_path)

        try:
                print("Running ABySS for {} and {}".format(fo, re))
                abyss_output = subprocess.check_output(["abyss-pe", "k={}".format(k_value), "name=abyss_result", "in={} {}".format(fo, re), "-C", output_subdir_path])
        except subprocess.CalledProcessError:
                print("ABySS could not finish the assembly. Please check the files.")
                return False

        print("Successfully ran ABySS for {} and {}".format(fo, re))
        return True



inp='/Users/rhiyasharma/Downloads/final_trim_output/test'
outp = '/Users/rhiyasharma/Downloads/abyss/new2/'

files = os.listdir(inp)
forward_file = []
reverse_file = []

for f in files:
        if f.endswith('_1.fastq'):
                forward_file.append(f)
        if f.endswith('_2.fastq'):
                reverse_file.append(f)

forward_file.sort()
reverse_file.sort()

k=33
# 21 55 77 33
for i in range(len(forward_file)):
        abyss_output = abyss_runner(forward_file, reverse_file, inp, outp, k)


if abyss_output is not True or None:
        print("Failed")
