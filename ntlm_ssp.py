import requests
import base64
import time
import argparse
import ssl
import struct
import urllib3 #Debug to remove cert warnings - remove before launch
import sys

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Debug to supress cert warnings...remove

#Required to force tls1_1 connections, else it goes to 1.0 which some servers dont support...blah. Thank you stack overflow! incase 1_1 doest work, switch to 1_2 etc...
class TLS_1_2(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
            self.poolmanager = PoolManager(num_pools=connections,
                               maxsize=maxsize,
                               block=block,
                               ssl_version=ssl.PROTOCOL_TLSv1_2)

def ntlm(data, begining):
	 A = begining+2
         B = struct.unpack("<H", data[begining:A])
         C = B[0]
	 return A,C

def domain(url, session):
	#Lets get some target inforamtion by abusing NTLMSSP messages with null parameters
	protected_dirs=['/', '/ews/', '/autodiscover/', '/Microsoft-Server-ActiveSync/', '/OAB/', '/Rpc/', '', ''] #NTLM Protected Directories 
	for directories in protected_dirs:
		owa = url+directories+''
		print "Trying "+owa+"..."
		header = {'Authorization':'NTLM TlRMTVNTUAABAAAAB4IIogAAAAAAAAAAAAAAAAAAAAAGAbEdAAAADw=='} #Null data, Type 1 Message
		request = session.get(owa,  headers=header, verify=False)

		try:
			Type_2 = request.headers["WWW-Authenticate"] #
			NTLMSSP = Type_2.replace("NTLM ", "")
			encoded = NTLMSSP.split(",", 1)
			break
		except:
			if directories =="/Rpc/":
				print "No NTLM protected directories found. Check the base url or manually confirm location"
				return
			print str(directories)+" Does not seem NTLM Protected, trying next!"
	try:
		info = base64.b64decode(encoded[0])
    	except:
        	print "Somethings funky, header not what was expected: " + NTLMSSP
        	return

	if info[:8] == "NTLMSSP\0":
        	print "Found NTLMSSP header"
		if info[40:42] =="\0": #Target info length should be here...if its not, or if its null, there is no information
			print("Information length is 0. There is no data coming.")
			return

		msg = struct.unpack("<i", info[8:12])
    		type = msg[0]
		print "Msg Type: " + str(type)

		I_offset = struct.unpack("<i", info[44:48])
                Offset = I_offset[0]

		#Product Version
		Major = struct.unpack("<B", info[48:49])
		Minor = struct.unpack("<B", info[49:50])
		Build = struct.unpack("<H", info[50:52])
                v1 = Major[0]
		v2 = Minor[0]
		v3 = Build[0]
		Product_Version = str(v1)+"."+str(v2)+"."+str(v3)

		#Domain Name
		D_Length_Offset = ntlm(info, Offset)
		D_Name_Length = ntlm(info, D_Length_Offset[0]) 
		Domain_Name = D_Name_Length[1] + D_Name_Length[0]
		Domain = info[D_Name_Length[0]:Domain_Name]

		#Host Name
		S_Length_Offset = ntlm(info, Domain_Name)
                S_Name_Length = ntlm(info, S_Length_Offset[0])
		Server_Name = S_Name_Length[1] + S_Name_Length[0]

		#DNS Domain Name
                DNS_Length_Offset = ntlm(info, Server_Name)
		DNS_Name_Length = ntlm(info, DNS_Length_Offset[0])
                DNS_Domain_Name = DNS_Name_Length[1] + DNS_Name_Length[0]

		#DNS Server Name
		Sub_Length_Offset = ntlm(info, DNS_Domain_Name)
                Sub_Name_Length = ntlm(info, Sub_Length_Offset[0])
                Sub_DNS_Domain_Name = Sub_Name_Length[1] + Sub_Name_Length[0]
		
		print "Domain Name:	 	 "+ Domain
		print "Host Name:	 	 "+info[S_Name_Length[0]:Server_Name]
		print "DNS Domain Name:	 "+info[DNS_Name_Length[0]:DNS_Domain_Name]
		print "DNS Server Name:	 "+info[Sub_Name_Length[0]:Sub_DNS_Domain_Name]
		print "Product Version:	 " + str(Product_Version)

	else:
        	print "NTLMSSP signature not found. Directory is not NTLM protected or something funky is happening."
		return

	return Domain

if __name__ == '__main__':

	Url = sys.argv[1]
	TLS = requests.Session()
	TLS.mount('https://', TLS_1_2())


	domain(Url, TLS)

#        main()

