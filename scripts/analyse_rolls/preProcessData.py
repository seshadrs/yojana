import sys
import extractVoterRules as RULES


def main():
	inputfi = open(sys.argv[1],'r')
	outputfi = open(sys.argv[2], 'w')
	validData = RULES.preProcessData(inputfi)
	for li in validData:
		outputfi.write(li+'\n')
	outputfi.close()

if __name__=="__main__":
	main()