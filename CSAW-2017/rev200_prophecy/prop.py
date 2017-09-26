from pwn import *
from struct import pack

def main():
    # r = remote('reversing.chal.csaw.io', 7668)
    r = process("./prophecy")
    
    print r.recvuntil(">>")
    r.send("BANANA_ME_CRAZY.starcraft\n")
    print r.recvuntil(">>")
    r.send(""
        + pack("<I", 0x17202508)
        + "AAA\0\0AAA"
        
        # 0x4A = I never look for trouble but it always seems to find me. Usually at a bar.
        # 0x4B = I do not join. I lead!
        # 0x4F = On a distant, shadowed world, the protoss will make their final stand.
        # 0x5A = With the Khala fallen to corruption, the memories of our ancestors are lost to us....
        + chr(0x4B)
        
        # 0x1 = In the fullness of time the cycle shall draw to its end
        # 0x2 = Every living thing in the universe will bow before the Queen of Blades, or else they will die. Obedience or oblivion. That is why we fight.
        # 0x3 = You'll see that better future Matt. But it 'aint for the likes of us.
        + chr(0x2)
        
        + "\x93\xea\xe4\0"
        + "ZERATUL"
        + "\0SAVED"
        + "AAAA"
    )
    
    print r.recvall()


if __name__ == '__main__':
    main()
