#include "fiducialXSTemplates.C"
#include <iostream>

using namespace std;


int main(int argc, char* argv[])
{
	if(argc != 10 && argc != 11)
		return 1;

    if(argc == 10)
    fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9]);

    if(argc == 11)
        fiducialXSTemplates(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10]);

	return 0;
}
