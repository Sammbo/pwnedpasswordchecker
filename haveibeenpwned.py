from urllib import request
import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("password")
args = parser.parse_args()

hasedPass = hashlib.sha1(str(args.password).encode('utf-8')).hexdigest()

url = "https://api.pwnedpasswords.com/range/{}".format(hasedPass[:5])

req = request.Request(url)
req.add_header('User-Agent','Pwned-Checker-Python')
response = request.urlopen(req).read()
response_dict  = dict(item.split(':') for item in response.decode("UTF-8").split('\r\n'))

match = False
match_key = None
for key in response_dict:
    if hasedPass[5:] == key.lower():
        match_key = key
        match = True
    if match == True:
        break

if match == True:
    print("Password Pwned!\nHacked {} times".format(response_dict[match_key]))
else:
    print('No Pwnage!')