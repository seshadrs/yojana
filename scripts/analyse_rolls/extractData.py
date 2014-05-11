import sys, os


def main():
	ROMANIZE_CMD = "./romanize_indic_text.py < %s > %s"
	CONVERT_CMD = "python extractVoterDatabase.py %s >> %s"

	dataPath = sys.argv[1]
	convert = []
	romanPath = dataPath+"/romanized"
	database = dataPath+"/"+"voterDatabase.txt"
	filePaths = []
	if os.path.exists(romanPath):
		os.popen("rm -r " + romanPath)
	if os.path.exists(database):
		os.popen("rm " + database)
	os.popen("mkdir %s" % romanPath)
	for fi in os.listdir(dataPath):
		if os.path.isdir(dataPath+"/"+fi):
			continue
		else:
			filePaths.append(dataPath+"/"+fi)
	for dfi in filePaths:
		print "Romanizing " + dfi
		outfile = romanPath+"/"+dfi.split("/")[-1]+".romanized"
		os.popen(ROMANIZE_CMD % (dfi, outfile))
		convert.append(outfile)
	for cfi in convert:
		print "Converting " + cfi
		os.popen(CONVERT_CMD % (cfi, database))


if __name__=="__main__":
	main()
