'''
Compares lcov coverage report files (.info) and reports coverage reductions
'''
import sys
import os

#define positions of coverage data stats in the list using enums
CovStatFields = {
	'FNF' : 0,
	'FNH' : 1,
	'BRF' : 2,
	'BRH' : 3,
	'LF'  : 4,
	'LH'  : 5
}
#For files without branches
TruncatedCovStatFields1 = {
	'FNF' : 0,
	'FNH' : 1,
	'LF'  : 2,
	'LH'  : 3
}
#For files without functions
TruncatedCovStatFields2 = {
	'LF'  : 0,
	'LH'  : 1
}

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

'''Compare the coverage statistics
There are several possible scenarios which can come during comparison.
For eg: 
1. You add a new file, it will show up in the coverage file which is not in referene
2. Code was refactored and all functions/branches in the code were removed
'''
def compareCoverageStats(fileName1, covReport1, fileName2, covReport2):
	isSameCodeCoverage = True
	covStatsList = [None, TruncatedCovStatFields2, TruncatedCovStatFields1, CovStatFields]

	print("*" * 50)
	print(bcolors.BOLD + "(Left):%s \t" %(fileName1), end = '')
	print("(Right):%s" %(fileName2) + bcolors.ENDC)
	print("*" * 50)

	if len(covReport1) > len(covReport2):
		print(bcolors.WARNING + "\t\t>>Warning ! Missing Files in coverage. Possibly refactored buildreport" + bcolors.ENDC)
		isSameCodeCoverage = False

	elif len(covReport2) > len(covReport1):
		print(bcolors.WARNING + "<<Warning ! Missing Files in coverage. Possibly refactored buildreport" + bcolors.ENDC)
		isSameCodeCoverage = False

	for key, list1 in covReport1.items():
		list2 = covReport2.get(key)

		if list2 == None:
			print(bcolors.WARNING + "\t\t>>Missing report for file %s" %key + bcolors.ENDC)
			continue

		listCovStatField = covStatsList[len(list2)//2]
		#Missing branch or function due to refactoring
		if len(list2) < len(list1):
			print(bcolors.WARNING + "\t>>Warning ! Missing branch/func cov. Possibly refactored file" + bcolors.ENDC)
			isSameCodeCoverage = isSameCodeCoverage and False
			continue
		#Missing branch or function due to refactoring
		elif len(list1) < len(list2):
			print(bcolors.WARNING + "<<Warning ! Missing branch/func cov. Possibly refactored file" + bcolors.ENDC)
			isSameCodeCoverage = isSameCodeCoverage and False
			continue
		#Two reports have the same fields. No refactoring
		else:

			if list2 != None and len(list2) == len(CovStatFields):
				#Function Coverage
				if list2[listCovStatField['FNH']] < list1[listCovStatField['FNH']]:
					print(bcolors.FAIL + "\t\t>>" "Function coverage reduced for %s" %key + bcolors.ENDC)
					isSameCodeCoverage = isSameCodeCoverage and False
				elif list1[listCovStatField['FNH']] < list2[listCovStatField['FNH']]:
					print(bcolors.FAIL + "<<Function coverage reduced for %s" %key + bcolors.ENDC)
					isSameCodeCoverage = isSameCodeCoverage and False
				#Line coverage
				if list2[listCovStatField['LH']] < list1[listCovStatField['LH']]:
					print(bcolors.FAIL + "\t\t>>" "Line coverage reduced for %s" %key + bcolors.ENDC)
					isSameCodeCoverage = isSameCodeCoverage and False
				elif list1[listCovStatField['LH']] < list2[listCovStatField['LH']]:
					print(bcolors.FAIL + "<<Line coverage reduced for %s" %key + bcolors.ENDC)
					isSameCodeCoverage = isSameCodeCoverage and False
				#Branch coverage
				if list2[listCovStatField['BRH']] < list1[listCovStatField['BRH']]:
						print(bcolors.FAIL + "\t\t>>" "Branch coverage reduced for %s" %key + bcolors.ENDC)
						isSameCodeCoverage = isSameCodeCoverage and False
				elif list1[listCovStatField['BRH']] < list2[listCovStatField['BRH']]:
						print(bcolors.FAIL + "<<Branch coverage reduced for %s" %key + bcolors.ENDC)
						isSameCodeCoverage = isSameCodeCoverage and False

			elif list2 != None and len(list2) == len(TruncatedCovStatFields1):

				if list2[listCovStatField['FNH']] < list1[listCovStatField['FNH']]:
					print(bcolors.FAIL + "\t\t>>" "Function coverage reduced for %s" %key + bcolors.ENDC)
					isSameCodeCoverage = isSameCodeCoverage and False
				elif list1[listCovStatField['FNH']] < list2[listCovStatField['FNH']]:
					print(bcolors.FAIL + "<<Function coverage reduced for %s" %key + bcolors.ENDC)
					isSameCodeCoverage = isSameCodeCoverage and False

				if list2[listCovStatField['LH']] < list1[listCovStatField['LH']]:
					print(bcolors.FAIL + "\t\t>>" "Line coverage reduced for %s" %key + bcolors.ENDC)
					isSameCodeCoverage = isSameCodeCoverage and False
				elif list1[listCovStatField['LH']] < list2[listCovStatField['LH']]:
					print(bcolors.FAIL + "<<Line coverage reduced for %s" %key + bcolors.ENDC)
					isSameCodeCoverage = isSameCodeCoverage and False

			elif list2 != None and len(list2) == len(TruncatedCovStatFields2):

				if list2[listCovStatField['LH']] < list1[listCovStatField['LH']]:
					print(bcolors.FAIL + "\t\t>>" "Line coverage reduced for %s" %key + bcolors.ENDC)
					isSameCodeCoverage = isSameCodeCoverage and False
				elif list1[listCovStatField['LH']] < list2[listCovStatField['LH']]:
					print(bcolors.FAIL + "<<Line coverage reduced for %s" %key + bcolors.ENDC)
					isSameCodeCoverage = isSameCodeCoverage and False

			else:
				print(bcolors.WARNING + "\t\t>>" "Missing coverge for %s" %key + bcolors.ENDC)
				isSameCodeCoverage = isSameCodeCoverage and False

	return isSameCodeCoverage


#Parse the coverage info and populate the above data structure
def parseCoverageInfo(fileName):
	# key(fileName) : [FNF, FNH , BRF, BRH, LF, LH]
	coverageDatastructure = {}
	keyVal = None
	state = 'endRecord'
	testRecStartDelim = "TN:unittests_result"
	testRecEndDelim = "end_of_record"
	testFileNameDelim = "SF:"
	funcStartDelim = "FNF:"
	funcEndDelim = "FNH:"
	branchStartDelim = "BRF:"
	branchEndDelim = "BRH:"
	lineStartDelim = "LF:"
	lineEndDelim = "LH:"
	coverageStats = []

	with open(fileName) as f:
		for line in f:
			if state == 'endRecord':
				#Start of coverage test record for a source file
				if line.__contains__(testRecStartDelim) == True:
					#Start of a test recor processing
					state = 'startRecord'

			elif state == 'startRecord':
				if line.__contains__(testRecEndDelim) == True:
					#End of a test record processing
					state = 'endRecord'
					#Update the (key, value) into the dictionary
					coverageDatastructure[keyVal] = coverageStats
					#Reset values
					keyVal = None
					coverageStats = []
				elif line.find(testFileNameDelim) != -1:
					#get the file name
					temp =  line[len(testFileNameDelim):].split('/')[-1]
					#replace the line break to get just the file name
					keyVal = temp.replace("\n", "")
				elif line.find(funcStartDelim) != -1:
					#Append Coverage stats to the list
					coverageStats.append(int(line[len(funcStartDelim):]))
				elif line.find(funcEndDelim) != -1:
					#Append Coverage stats to the list
					coverageStats.append(int(line[len(funcEndDelim):]))
				elif line.find(branchStartDelim) != -1:
					#Append Coverage stats to the list
					coverageStats.append(int(line[len(branchStartDelim):]))
				elif line.find(branchEndDelim) != -1:
					#Append Coverage stats to the list
					coverageStats.append(int(line[len(branchEndDelim):]))
				elif line.find(lineStartDelim) != -1:
					#Append Coverage stats to the list
					coverageStats.append(int(line[len(lineStartDelim):]))
				elif line.find(lineEndDelim) != -1:
					#Append Coverage stats to the list
					coverageStats.append(int(line[len(lineEndDelim):]))

	return coverageDatastructure

#Get the coverage files from the provided directory
def GetUnitTestCoverageFiles(inputDir):
	coverageFiles = []

	for file in os.listdir(inputDir):
		if file.endswith(".info"):
			coverageFiles.append(file)

	return coverageFiles

if __name__ == '__main__':

	argLength = len(sys.argv)
	coverageStatistics1 = None
	coverageStatistics2 = None
	inputDirectory = None
	fileName1 = None
	fileName2 = None

	if argLength < 2:
		sys.exit("Usage: coverage_compare.py <Directory path > or coverage_compare.py <Reference coverage info> <Info file to be verified>")

	elif argLength > 2:
		#Argument contains 2 file names. First one is the referene coverage and the other one is the coverage file to be verified
		fileName1 = sys.argv[1]
		fileName2 = sys.argv[2]

	else:
		inputDirectory = sys.argv[1]
		coverageFilesinDir = GetUnitTestCoverageFiles(inputDirectory)
		if len(coverageFilesinDir) < 2:
			sys.exit("Error: Reference and Coverage file should be placed in the given directory. Please retry!")

		if inputDirectory[-1] != "/":
			inputDirectory = inputDirectory + "/"

		#Note that if there are more files in the directory, only the first two are picked
		fileName1 = inputDirectory + coverageFilesinDir[0]
		fileName2 = inputDirectory + coverageFilesinDir[1]

	coverageStatistics1 = parseCoverageInfo(fileName1)
	coverageStatistics2 = parseCoverageInfo(fileName2)

	print("*" * 50)
	isSameCodeCoverage = compareCoverageStats(fileName1, coverageStatistics1, fileName2, coverageStatistics2)

	if(isSameCodeCoverage == True):
		print(bcolors.OKGREEN + "Coverage results remains the same" + bcolors.ENDC)

	print("*" * 50)