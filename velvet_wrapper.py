#!/usr/bin/env python
import subprocess
import os


def velvet_runner(fastq_file_forward, fastq_file_reverse, kmer, input_directory_path, output_directory_path):
	'''
	This function has been written by Shuting Lin.

	os.system("cat "+r1+" "+r2+" > "+x+"_unpaired.fq")
	os.system("velveth "+root+"/assem"+str(kmer)+" "+str(kmer)+" -shortPaired -fastq -separate "+r1+" "+r2+ ' -short2 '+x+"_unpaired.fq")
	os.system("velvetg "+root+"/assem"+ str(kmer) +" -min_contig_lgth 500")
	os.system("cp "+root+"/assem"+str(kmer)+"/contigs.fa "+root+"/velvet_results/"+x+".fa")
	os.system("rm "+x+"_unpaired.fq")
	'''

	#Modified version by Shivam Sharma.

	#Create file paths.
	fastq_file_forward_path = input_directory_path + fastq_file_forward
	fastq_file_reverse_path = input_directory_path + fastq_file_reverse

	#Creating a directory inside output directory.
	output_subdir_name = fastq_file_forward.split('.')[0].split('_')[0]
	output_subdir_path = output_directory_path.rstrip('/') + '/' + output_subdir_name 

	#Check if subdir is already there.
	if not output_subdir_name in os.listdir(output_directory_path):
		os.mkdir(output_subdir_path)

	#Execute Velvet.
	try:
		print("Running velvet for {} and {}".format(fastq_file_forward, fastq_file_reverse))
		
		#Tried hard to not use os.system(). But alternative options are very long.
		#If other members want, they can make this change.
		#Concating files.
		os.system("cat " + fastq_file_forward_path + " " + fastq_file_reverse_path + " > " + output_subdir_path + '/' + output_subdir_name + "_unpaired.fq")

		#Calling velveth.
		assem_path = output_subdir_path + "/" + "assem" + str(kmer)

		if not os.path.exists(assem_path):
			os.mkdir(assem_path)

		velveth_output = subprocess.check_output(["velveth", assem_path, str(kmer), "-shortPaired", "-fastq", "-separate", fastq_file_forward_path, fastq_file_reverse_path, '-short2', '-fastq', output_subdir_path + '/' + output_subdir_name + "_unpaired.fq"])
		velvetg_output = subprocess.check_output(["velvetg", assem_path, "-min_contig_lgth", "500"])

		#Delete the concatenated file.
		delete_cat_file = subprocess.check_output(["rm", output_subdir_path + '/' + output_subdir_name + "_unpaired.fq"])

	except subprocess.CalledProcessError as e:
		print("Velvet could not finish the assembly. Please check the files.")
		print("Error thrown: {}".format(e.output))
		return False

	print("Successfully ran velvet for {} and {}".format(fastq_file_forward, fastq_file_reverse))
	return True


	
if __name__ == "__main__":
	main()


