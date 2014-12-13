#include "fiducialXSTemplates.C"
#include <iostream>

using namespace std;


int main(int argc, char* argv[])
{
	if(argc != 12)
		return 1;
	
	fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10], argv[11]);
	return 0;
}
