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
    k=91

local = args.file_directory
os.chdir(local)
trim_file=os.listdir(os.getcwd())
name=[]
for i in trim_file:
	c=i.split(".")
	if c[1]=='fastq':
		name.append(i)

#print(len(name))
root=os.path.abspath(os.path.join(os.getcwd(), ".."))

def mkdir(result_folder):
    
    create= root+str("/")+result_folder
    f = os.path.exists(create)
    if not f:                 
        os.makedirs(create)

mkdir("velvet_results")
#print(root)

sample=[]
for v in name:
    v=v.split("_")[0]
    sample.append(v)
sample=list(set(sample))
#print(sample)

def run_velvet(r1,r2,kmer):
    os.system("cat "+r1+" "+r2+" > "+x+"_unpaired.fq")
    os.system("velveth "+root+"/assem"+str(kmer)+" "+str(kmer)+" -shortPaired -fastq -separate "+r1+" "+r2+ ' -short2 '+x+"_unpaired.fq")
    os.system("velvetg "+root+"/assem"+ str(kmer) +" -min_contig_lgth 500")
    os.system("cp "+root+"/assem"+str(kmer)+"/contigs.fa "+root+"/velvet_results/"+x+".fa")
    os.system("rm "+x+"_unpaired.fq")

for x in sample:
    pair=[]
    for y in name:
        if x in y:
            pair.append(y)

    res=run_velvet(pair[0],pair[1],k)

if __name__ == "__main__":
    main()


