from urllib import request
import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p','-password', help='stores the password for testing',action='store',dest='password')
parser.add_argument('-v','--verbose', help='increase output verbosity',action='store_true',default=False)
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

if args.verbose == True:
    for key in response_dict:
        print("{0}{1} : {2}".format(hasedPass[:5],key,response_dict[key]))

print('\n\n')

if match == True:
    print("Password Pwned!\nHacked {} times".format(response_dict[match_key]))
else:
    print('No Pwnage!')