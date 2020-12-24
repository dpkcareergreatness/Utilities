## Introduction
This script generates a suppression file for valgrind's memcheck. To generate 
suppresion file, run valgrind with the extra option --gen-suppressions=all --log-file=out.txt.
This tells valgrind to print a suppression after every error it finds. 
You now have a file containing the raw output, with the suppressions mingled with the errors and other stuff. 
Also, as errors are usually multiple, there'll usually be multiple instances of each suppression.

So pass the output from valgrind to this script. The script parses the output file and gets the suppression rules
and removes duplicates from it.

For more details on valgrind suppression refer: https://wiki.wxwidgets.org/Valgrind_Suppression_File_Howto

# Steps for using valgrind suppression file
1. Run valgrind 
	valgrind --leak-check=full --show-reachable=yes --error-limit=no --gen-suppressions=all --log-file=out.txt <App to memcheck> [App arguments]
2. Run the output of valgrind(out.txt) through this script
	valgrindGenerateSuppression.py <output file from valgrind> <Fullpath and File name where you want supp. file to be saved>
3. Run valgrind with the suppression file to suppress the errors
	valgrind --leak-check=full --show-reachable=yes --error-limit=no --suppressions=<Path to supp. file> --log-file=out.txt <App to memcheck> [App arguments]

