# Requires pdfminer

import os,sys, glob
from subprocess import call

input_dir = os.path.abspath(sys.argv[1])
output_dir = os.path.abspath(sys.argv[2])

os.chdir(input_dir)
for pdf_file_name in glob.glob("*.pdf"):
	op_file= pdf_file_name+'.txt'
	print 'EXECUTING pdf2txt.py '+os.path.join(input_dir,pdf_file_name)+' > '+os.path.join(output_dir,op_file)
	os.popen('pdf2txt.py '+os.path.join(input_dir,pdf_file_name)+' > '+os.path.join(output_dir,op_file))
