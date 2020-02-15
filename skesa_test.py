#!/usr/bin/env python

def main():
    '''
    Insert argparse code that populates the following variables
     - reads directory
     - k-mer value
     
    '''
    # Argparse code

import argparse
import os 

parser=argparse.ArgumentParser()

parser.add_argument("-folder","--file_directory",help="this is the file directory")
parser.add_argument("-k","--kmer",help="setup k value")

args=parser.parse_args()

if args.kmer:
    k=args.kmer
else:
    k=21

local = args.file_directory
os.chdir(local)
trim_file=os.listdir(os.getcwd())
name=[]
for i in trim_file:
        c=i.split(".")
        if c[1]=='fastq':
                name.append(i)

#print((name))
root=os.path.abspath(os.path.join(os.getcwd(), ".."))

def mkdir(result_folder):

    create= root+str("/")+result_folder
    f = os.path.exists(create)
    if not f:
        os.makedirs(create)

#print(root)

sample=[]
for v in name:
    v=v.split("_")[0]
    u=v.split("output")[0]
    sample.append(u)
sample=list(set(sample))
#print(sample)

def run_skesa(r1,r2,kmer=21):


    os.system("skesa --fastq "+ r1+" "+r2 + " --contigs_out " +root+"/skesa_results/"+x+"/contigs.fasta" +" --kmer "+str(kmer)+ " --min_contig 500")
    #os.system("skesa --fastq "+ r1+" "+r2 + " --contigs_out " +root+"/contigs.fasta" +" --kmer "+str(kmer)+ " --min_contig 500")


for x in sample:
    mkdir("skesa_results/"+x)
    pair=[]
    for y in name:
        if x in y:
            pair.append(y)
    run_skesa(pair[0],pair[1],k)




if __name__ == "__main__":
    main()


