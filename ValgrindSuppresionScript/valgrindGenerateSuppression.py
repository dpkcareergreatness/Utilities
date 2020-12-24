#!/usr/bin/python
'''
Generates suppression files for valgrind from valgrinds raw output file
'''
import sys

def writeFile(outputFileName, string):
	with open(outputFileName, 'w')as f:
		f.write(string)


sup_dict = {}
def checkUniqueness(string):
	retVal = True

	hash_val = hash(string)
	if(sup_dict.get(hash_val, None) != None):
		# Not a unique value
		retVal = False
	else:
		#Update dict
		sup_dict[hash_val] = string

	return retVal


def parseValgrindOutput(inputFileName):
	outlines = ''
	enableLogging = False

	temp = ''

	with open(inputFileName, 'r') as f:

		while True:
			line = f.readline()

			#EOF reached
			if not line:
				break

			if line == '{\n':
				enableLogging = True
			elif line == '}\n':
				temp += line
				enableLogging = False

			if enableLogging == True:
				temp += line

			#There is something in temp and we need to check if it is unique
			if temp != '' and enableLogging == False:
				val = checkUniqueness(temp)
				if val == True:
					outlines += temp
				#Reset temp
				temp = ''

	return outlines

if __name__ == '__main__':
	ipFile = sys.argv[1]
	opFile = sys.argv[2]
	out = parseValgrindOutput(ipFile)
	writeFile(opFile, out)
