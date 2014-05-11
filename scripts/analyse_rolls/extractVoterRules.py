import re

#ignore all lines from start of filenuntil we see this pattern
START_LINE_PATTERN=re.compile("^([A-Z]\w{9,9})$")#("^\d\d$")

#stop processing data after this line
END_LINE_PATTERN=re.compile("aayu \d\d\.\d\d\.\d\d\d\d.*") 


VOTER_DATA_PATTERN={
	#0: re.compile("^(\d\d)$"), #formid
	0: re.compile("^(\w{10,10})$"), #voterId
	1: re.compile("^matadaataa kaa naam: (.*)$"), #voterName
	2: re.compile("^ilang (.*)$"), #voterGender
	3: re.compile("(.*) kaa naam: (.*)"), #voterRelation, relationName
	4: re.compile("makaan .+ (\d+) aayu (\d+)") #houseNumber, age
}

DATA_REPEAT_SIZE = 18
VOTER_SIZE = 5

GENDERS={
	'm\xc7\x91halaa' : "F",
	'pu\xc7\xbesh' : "M"
}

RELATIONS={
	'\xc7\x92pataa' : "Father",
	"pit" : "Husband"
}


class Voter:
	def __init__(self, (formId, voterId, voterName, voterGender,
		voterRelation, otherDetails)):
		self.formId = formId
		self.voterId = voterId[0]
		self.voterName = voterName[0]
		if voterGender[0] not in GENDERS:
			self.voterGender = "UNDEF" + voterGender[0]
		else:
			self.voterGender = GENDERS[voterGender[0]]
		if voterRelation[0] not in RELATIONS:
			self.voterRelation = "UNDEF:" + voterRelation[0]
		else:
			self.voterRelation = RELATIONS[voterRelation[0]]
		self.relationName = voterRelation[1]
		self.houseNumber = otherDetails[0]
		self.voterAge = otherDetails[1]
	def printVoter(self):
		s = [self.formId, self.voterId, self.voterName, self.voterGender, self.voterAge,
			self.voterRelation, self.relationName, self.houseNumber]
		print ",".join([str(dt) for dt in s])


def preProcessData(fi):
	validLines = []
	for li in fi:
		li = li.strip()
		for pat in VOTER_DATA_PATTERN.values():
			if pat.match(li):
				validLines.append(li)
				break
	return validLines


