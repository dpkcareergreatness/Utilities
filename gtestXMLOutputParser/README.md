## gtestcoverage results xml parser
This script parses the GTEST_OUT xml's generated by running google tests and reports failures on the screen. 
Useful when there are lots of tests clogging the console

eg: gtestresultxmlparser.py <gtestxmlPath> <outputfileFullPath>

Also, when [gtest-parallel](https://github.com/google/gtest-parallel) is used, the gtest out xmls are malformed.
This script can repair the malformed xml and parse it correctly.
