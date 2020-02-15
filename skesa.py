#!/usr/bin/env python
import subprocess
import os


def skesa_runner(fastq_file_forward, fastq_file_reverse, kmer, input_directory_path, output_directory_path):
        '''
        This function has been written by Shuting Lin.

        os.system("cat "+r1+" "+r2+" > "+x+"_unpaired.fq")
        os.system("skesah "+root+"/assem"+str(kmer)+" "+str(kmer)+" -shortPaired -fastq -separate "+r1+" "+r2+ ' -short2 '+x+"_unpaired.fq")
        os.system("skesag "+root+"/assem"+ str(kmer) +" -min_contig_lgth 500")
        os.system("cp "+root+"/assem"+str(kmer)+"/contigs.fa "+root+"/skesa_results/"+x+".fa")
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

        #Execute skesa.
        try:
                print("Running skesa for {} and {}".format(fastq_file_forward, fastq_file_reverse))

                #Tried hard to not use os.system(). But alternative options are very long.
                #If other members want, they can make this change.
                #Concating files.

                #Calling skesah.

                skesah_output = subprocess.check_output(["skesa --fastq "+ fastq_file_forward_path+" "+fastq_file_reverse_path + " --contigs_out " +output_subdir_path+"/"+ output_subdir_name +" --kmer 21 --min_contig 500"])

        except subprocess.CalledProcessError as e:
                print("skesa could not finish the assembly. Please check the files.")
                print("Error thrown: {}".format(e.output))
                return False

        print("Successfully ran skesa for {} and {}".format(fastq_file_forward, fastq_file_reverse))
        return True


if __name__ == "__main__":
        main()

