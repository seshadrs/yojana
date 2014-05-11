import sys
import extractVoterRules as RULES

def matchPatterns(li):
	for index in RULES.VOTER_DATA_PATTERN:
		pat = RULES.VOTER_DATA_PATTERN[index]
		matchd = pat.match(li)
		if matchd:
			data = matchd.groups()
			#print str(index) + "\t" + str(data)
			return (index, data)
	return (-1, -1)

def extractVoters(lines):
	started = 0
	atStart = 0
	flipId = 0
	voterDB = []
	voterCache = []
	globalId = 1
	for li in lines:
		li = li.strip()
		if RULES.START_LINE_PATTERN.match(li):
			started = 1
			atStart = 1
		elif RULES.END_LINE_PATTERN.match(li):
			for rem in voterCache:
				print rem
				itm = [i for i in rem]
				voterDB.append(RULES.Voter(tuple(itm)))
				print "here"
			return voterDB
		if started == 1:
			dataIndex, dataPoint = matchPatterns(li)
			if dataIndex == -1:
				continue
			else:
				if atStart:
					voterCandidate = [-1 for i in range(0, RULES.VOTER_SIZE)]
					atStart = 0
					curr = voterCandidate.pop(dataIndex)
					if (curr == -1):
						voterCandidate.insert(dataIndex, dataPoint)
					else:
						print "non -1 value at start"
					voterCache.append(voterCandidate)
				else:
					localIndex = 0
					while localIndex < len(voterCache):
						voterCandidate = voterCache.pop(localIndex)
						curr = voterCandidate.pop(dataIndex)
						if (curr == -1):
							voterCandidate.insert(dataIndex, dataPoint)
							if voterCandidate.count(-1) > 0:
								voterCache.insert(localIndex, voterCandidate)
							else: #filled all params, add voter to cache
								voterCandidate.insert(0, globalId)
								globalId += 1
								newVoter = RULES.Voter(tuple(voterCandidate))
								voterDB.append(newVoter)
							break
						else:
							voterCandidate.insert(dataIndex, curr)
							voterCache.insert(localIndex, voterCandidate)
						localIndex += 1
	return voterDB



def main():
	inputfi = open(sys.argv[1],'r')
	lines = RULES.preProcessData(inputfi)
	voters = extractVoters(lines)
	for i in voters:
		i.printVoter()

if __name__=="__main__":
	main()
