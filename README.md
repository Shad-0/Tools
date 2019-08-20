# Drupal IP Block
The Drupal-IP-Block.py script was created to demonstrate the flaws in implementing blocks per IP vs accounts. It takes a username file and a password file, and attempt to login with every possible 
combination. In my case, the block was implemented after 4 attempts, so I leveraged Tor to change the exit node every 3 tries, therefore allowing me to bypass the block and bruteforce the account.
Note that the ** credentials you send over Tor can be seen by the exit node, and as such can be intercepted **. This script was written as a proof of concept,and should not be used in production systems.

###### To Do:
- Add the ability to choose between Drupal, Joomla, Wordpress, or custom forms.

# Evasion.c
The Evasion.c script was something I used in up to 2016 to obfuscate my payloads, and back then it was FUD. Today it is caught by more and more engines, although it is still a good starting point if like me
you arent a fan/dont have much success with frameworks like Veil. The script is a combination of three methods discussed in a paper by Emeric Nasi, disclosed as one of the files from the Vault 7 CIA leaks. 
The paper can be found [here](https://wikileaks.org/ciav7p1/cms/files/BypassAVDynamics.pdf). The Three nested and employed techniques in the script were
###### 6.1 "Offer you have to refuse"
###### 6.1 "Hundred Million Increments"
###### 6.5 "What is my name"

Note, during my testing I found that exe's compiled in Linux with something like mingw were automatically flagged. Instead, compile on windows, using something like Dev C++
###### To Do:
- Update with FUD methods (although likely wont share for a while ;) )

# ntlm_ssp.py
The ntlm_ssp.py script is part of a bigger project im working on, which extracts domain information from NTLMSSP type 2 messages. The script takes a URL as an argument and checks for default NTLM protected directories
found in Exchange servers, such as /ews/ and /autodiscover/. Note that the script will also try the base url given, incase the url provided is not an Exchange server. Once an NTLMSSP message is found, it will
output the domain name, host name, dns domain name and server product number.


# reverse_tcp.c
This was another script I used when attempting to bypass end point AVs. This would simply connect back on 443 and spawn a command shell. 
*** NOTE: I DID NOT WRITE THIS! *** at the time i got it from somewhere on the web, likely someones github page. I may have added/removed sections and changed variable names 
in an effort to bypass signatures. Its here because it may serve as a starting point for someone else.
