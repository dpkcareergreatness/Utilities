import time
import sys
import os
import re
# import only system from os 
from os import system, name 
  
# import sleep to show output for some time period 
from time import sleep 

import xml.etree.cElementTree as ET

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

#Write Test results to output file
def writeTestOutput(outputfilePath, testName, testStatus):
	if os.path.exists(outputfilePath):
		append_write = 'a' # append if already exists
	else:
		append_write = 'w' # make a new file if not

	with open(outputfilePath, append_write) as f:
		f.write(testName+" : "+ testStatus)
		f.write("\n")

#gtest-parallel causes a malformed xml by adding a garbage line tag.in GTEST_OUT xml
#This xml error can be fixed with a little post processing
def repairXML(file_name, errorString):
	bFixPossible = True

	pattern = r'line \d'
	match = re.search(pattern, errorString)
	if not match:
		bFixPossible = False
	else:
		_,lineNumber = match.group().split(' ')
		lineNumber = int(lineNumber)
		xmlData = ''
		line = 1

		with open(file_name, 'r') as f:
			temp = f.readline()
			#Loop till EOF
			while temp:
				#Skip the line containing the malformed xml line
				if line != lineNumber:
					xmlData += temp
				temp = f.readline()
				line += 1

		#Write back the correct xml back to the file
		with open(file_name, 'w') as f:
			f.write(xmlData)

	return bFixPossible

#gtest creates an xml report for each test run.
#gtest xml is of below format:
#<testsuites tests="38" failures="0" disabled="0" errors="0" timestamp="2020-08-18T20:35:17" time="0.007" name="AllTests">
#This is in the root attribute itself so thats all we need to parse
def parseXML(file_name, outputfilePath):
	try:
		# Parse XML with ElementTree
		tree = ET.ElementTree(file=file_name)
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print("Malformed xml in {}".format(file_name))
		bFixPossible = repairXML(file_name, str(exc_obj))
		#Retry if the error could be fixed by the repair method
		if bFixPossible:
			parseXML(file_name, outputfilePath)
	else:
		root = tree.getroot()
		#Assign the tag attributes
		d = root.attrib

		#Check if there are any failures
		failedCount = 0
		testName = file_name.split("/")[-1]
		testStatus = "Passed"
		if d.get("failures") != '0':
			print("*" * 25 )
			failedCount += 1
			print(bcolors.FAIL + "%d Failed tests %s" %(failedCount, testName) + bcolors.ENDC)
			print("*" * 25 )
			testStatus = "Failed"

		#Write Test summary to output fie
		writeTestOutput(outputfilePath, testName, testStatus)

# define screen clear function 
def clear(): 
	# for windows 
	if name == 'nt': 
		ret = system('cls') 
	# for linux( os.name is 'posix') 
	else: 
		ret = system('clear')

#Main code
#Check commandline for output path
if len(sys.argv) < 3:
	sys.exit("Missing param! Use testresultparser.py <unittestxmlPath> <outputfileFullPath>")
else:
	testLogsPath = str(sys.argv[1])
	outputFileName = str(sys.argv[2])
	#clear screen
	clear()

	if not os.path.isdir(testLogsPath):
		os.mkdir(testLogsPath)

	for file in os.listdir(testLogsPath):
		if file.endswith(".xml"):
			print(file)
			parseXML(testLogsPath + "/" + file, outputFileName)
