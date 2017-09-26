from subprocess import Popen, PIPE, STDOUT

valid = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
for x in valid:
    for y in valid:
        test = 'aaaac'+x+y+'7'
        
        p = Popen(["./monkeyDo", "simple.banana"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        out = p.communicate(input=test)[0][:-1]
        
        if all(c in valid for c in out):
            if out.count("{") == 1 and out.count("}") == 1:
                if out[-2] == 's':
                    print out
