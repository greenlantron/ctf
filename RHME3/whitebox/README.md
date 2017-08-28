## White Box Unboxing (Crypto, 1 point)

    Here is a binary implementing a cryptographic algorithm. You provide an input and it produces the corresponding output. Can you extract the key?

This challenge gave me the most trouble of them all and then magically worked when I switched environments... Whitebox cryptography is the idea of precomputing and otherwise obfuscating encryption so it can be done safely and securely (heh) on otherwise unsafe machines without revealing the cipher key. The binary is simply [whitebox](whitebox).

As with all analysis challenges such as this the first step is doing our research and reading up on past writeups. In doing so we find the [SideChannelMarvels](https://github.com/SideChannelMarvels) github repository providing plenty of tools for analysis based attacks such as this. [Deadpool](https://github.com/SideChannelMarvels/Deadpool) can be used to extract keys in whitebox challenges via Differential Computational Analysis (DCA) or Differential Fault Analysis (DFA) and even includes writeups for just that. _I attempted DCA and did not make quantifiable progress, other writeups for challenges mention the inability of DCA so I focused purely on DFA._ We will be using DFA found and explained [here](https://github.com/SideChannelMarvels/Deadpool/blob/master/README_dfa.md).

---

In order to use deadpool and perform DFA we need our whitebox tables as a file for corruption. First we need to dump that area of memory with gdb via `dump memory mem.dump 0x6650C0 0x68A1C0`. Secondly we must modify our executable to now load the corrupted data. We can write some code to do just that and compile it using `scc`(shellcode compiler) that comes with the great [binary ninja](https://binary.ninja/). A quick patch later with the addresses from IDA we are in business.

```c
void main() {
    int fd = open("wb_data", O_RDONLY, 0);
    read(fd, (void*)0x6650C0, 0x25100);
}
```

```
$ cp whitebox wb_patched
$ scc --arch x64 read.c -o read.out
Output is 51 bytes
$ dd if=read.out of=wb_patched obs=1 seek=406434 conv=notrunc
0+1 records in
51+0 records out
51 bytes copied, 0.000102629 s, 497 kB/s
```

With the executable prerequisites setup let's run create our python script to perform the attack. We can copy an existing script from another challenge [here](https://github.com/SideChannelMarvels/Deadpool/blob/master/wbs_aes_ches2016/DFA/attack_ches2016.py) and make some small modifications. Let's first change our arguments for targetbin, targetdata, and goldendata to match our filenames. We will also be using phoenixAES for our DFA analysis so that can be left as it. The functions processinput and processoutput must be changed to match the format our binary expects. Those are the bare minimum arguments we need so we'll toss out anything else for now. Once we have these steps done we can run the script and fix any issues that pop up.

```python
import sys, os
import deadpool_dfa
import phoenixAES

def processinput(iblock, blocksize):
    return (bytes.fromhex('%0*x' % (2*blocksize, iblock)), ["--stdin"])

def processoutput(output, blocksize):
    return int(b''.join([x for x in output.split()]), 16)

engine=deadpool_dfa.Acquisition(targetbin='./wb_patched', targetdata='./wb_data', goldendata='./mem.dump', dfa=phoenixAES, processinput=processinput, processoutput=processoutput)
tracefiles_sets=engine.run()
for tracefile in tracefiles_sets[0]:
    if phoenixAES.crack(tracefile, verbose=1):
        break
```

```
$ ./attack_dfa.py
Press Ctrl+C to interrupt
Send SIGUSR1 to dump intermediate results file: $ kill -SIGUSR1 42435
Lvl 011 [0x00024198-0x000241A0[ xor 0x3D 74657374746573747465737474657374 -> 896D9871EDC6375E0F3FBB189B4AF219 GoodEncFault Column:3 Logged
Lvl 011 [0x00024198-0x000241A0[ xor 0xC2 74657374746573747465737474657374 -> 896D9879EDC65E5E0F34BB18164AF219 GoodEncFault Column:3 Logged
Lvl 011 [0x00024198-0x000241A0[ xor 0xD4 74657374746573747465737474657374 -> 896D98A4EDC68A5E0FDFBB185C4AF219 GoodEncFault Column:3 Logged
Lvl 011 [0x00024198-0x000241A0[ xor 0x1E 74657374746573747465737474657374 -> 896D985AEDC6C45E0FC4BB18574AF219 GoodEncFault Column:3 Logged
Lvl 012 [0x00022348-0x00022350[ xor 0xB7 74657374746573747465737474657374 -> 89CB983B15C6275E0F7BBBA8DF4A7619 GoodEncFault Column:1 Logged
Lvl 012 [0x00022348-0x00022350[ xor 0x5E 74657374746573747465737474657374 -> 891A983BC5C6275E0F7BBB66DF4A4519 GoodEncFault Column:1 Logged
Lvl 012 [0x00022348-0x00022350[ xor 0x20 74657374746573747465737474657374 -> 896C983B8FC6275E0F7BBB5BDF4A5319 GoodEncFault Column:1 Logged
Lvl 012 [0x00022348-0x00022350[ xor 0x79 74657374746573747465737474657374 -> 894C983B7CC6275E0F7BBBF4DF4A9619 GoodEncFault Column:1 Logged
Lvl 012 [0x000236A8-0x000236B0[ xor 0x42 74657374746573747465737474657374 -> 896DB83BED92275EBA7BBB18DF4AF238 GoodEncFault Column:2 Logged
Lvl 012 [0x000236A8-0x000236B0[ xor 0x31 74657374746573747465737474657374 -> 896DEE3BED67275E617BBB18DF4AF2FB GoodEncFault Column:2 Logged
Lvl 012 [0x000236A8-0x000236B0[ xor 0x3F 74657374746573747465737474657374 -> 896DEE3BEDDF275E6F7BBB18DF4AF279 GoodEncFault Column:2 Logged
Lvl 012 [0x000236A8-0x000236B0[ xor 0xC7 74657374746573747465737474657374 -> 896D903BED83275E7D7BBB18DF4AF2AB GoodEncFault Column:2 Logged
Lvl 012 [0x00021C58-0x00021C60[ xor 0xE3 74657374746573747465737474657374 -> 776D983BEDC627B80F7BF418DF1FF219 GoodEncFault Column:0 Logged
Lvl 012 [0x00021C58-0x00021C60[ xor 0x6B 74657374746573747465737474657374 -> 6D6D983BEDC6273D0F7BA118DF5BF219 GoodEncFault Column:0 Logged
Lvl 012 [0x00021C58-0x00021C60[ xor 0xDB 74657374746573747465737474657374 -> AF6D983BEDC627820F7B9718DF2DF219 GoodEncFault Column:0 Logged
Lvl 012 [0x00021C58-0x00021C60[ xor 0x46 74657374746573747465737474657374 -> 156D983BEDC6277E0F7BCA18DF3EF219 GoodEncFault Column:0 Logged
$
```

Hmm, we get some GoodEncFault's but no key.

---

Let's continue reading some other writeups and looking at the other arguments. The writeup for [kryptologik](https://github.com/SideChannelMarvels/Deadpool/blob/fa6475fd953a7654447315ec27a15731d4ddf5d6/wbs_aes_kryptologik/DFA/attack_kryptologik_last_round.py) gives us some information on the arguments we need. Let's add the maxleaf arguments and minleaf.

```python
engine=deadpool_dfa.Acquisition(targetbin='./wb_patched', targetdata='./wb_data', goldendata='./mem.dump',
       dfa=phoenixAES, processinput=processinput, processoutput=processoutput,
       maxleaf=0x100, minleaf=0x1,
)
```

That doesn't work either. Reading more we see there is an additional argument _minleafnail_, let's toss that in so _minleaf_ can actually go as low as 1.


```python
engine=deadpool_dfa.Acquisition(targetbin='./wb_patched', targetdata='./wb_data', goldendata='./mem.dump',
       dfa=phoenixAES, processinput=processinput, processoutput=processoutput,
       maxleaf=0x100, minleaf=0x1, minleafnail=0x1
)
```

```
$ ./attack_dfa.py
Press Ctrl+C to interrupt
Send SIGUSR1 to dump intermediate results file: $ kill -SIGUSR1 34361
Lvl 008 [0x00000067-0x00000068[ xor 0x2A 74657374746573747465737474657374 -> 896D9803EDC69B5E0F05BB18FC4AF219 GoodEncFault Column:3 Logged
Lvl 008 [0x00000067-0x00000068[ xor 0xBD 74657374746573747465737474657374 -> 896D9850EDC6735E0FD2BB18614AF219 GoodEncFault Column:3 Logged
Lvl 008 [0x00000067-0x00000068[ xor 0x71 74657374746573747465737474657374 -> 896D982DEDC6F45E0F53BB18AE4AF219 GoodEncFault Column:3 Logged
Lvl 008 [0x00000067-0x00000068[ xor 0x51 74657374746573747465737474657374 -> 896D98A0EDC6575E0FD7BB18144AF219 GoodEncFault Column:3 Logged
Lvl 008 [0x00000074-0x00000075[ xor 0x91 74657374746573747465737474657374 -> D66D983BEDC6276A0F7BC318DF24F219 GoodEncFault Column:0 Logged
Lvl 008 [0x00000074-0x00000075[ xor 0x48 74657374746573747465737474657374 -> 866D983BEDC627D00F7BDD18DFD1F219 GoodEncFault Column:0 Logged
Lvl 008 [0x00000074-0x00000075[ xor 0x9E 74657374746573747465737474657374 -> A46D983BEDC627FB0F7B2018DF3EF219 GoodEncFault Column:0 Logged
Lvl 008 [0x00000074-0x00000075[ xor 0xF6 74657374746573747465737474657374 -> D26D983BEDC627370F7B2818DFD7F219 GoodEncFault Column:0 Logged
Lvl 008 [0x0001D1DE-0x0001D1DF[ xor 0xDA 74657374746573747465737474657374 -> 896DA53BEDFA275E7B7BBB18DF4AF292 GoodEncFault Column:2 Logged
Lvl 008 [0x0001D1DE-0x0001D1DF[ xor 0xC4 74657374746573747465737474657374 -> 896D173BED61275E677BBB18DF4AF289 GoodEncFault Column:2 Logged
Lvl 008 [0x0001D1DE-0x0001D1DF[ xor 0x53 74657374746573747465737474657374 -> 896D653BED6E275E2C7BBB18DF4AF244 GoodEncFault Column:2 Logged
Lvl 008 [0x0001D1DE-0x0001D1DF[ xor 0x5B 74657374746573747465737474657374 -> 896D7F3BED29275E2F7BBB18DF4AF2F1 GoodEncFault Column:2 Logged
Lvl 008 [0x0001D1DF-0x0001D1E0[ xor 0xD5 74657374746573747465737474657374 -> 8906983B99C6275E0F7BBB36DF4A6D19 GoodEncFault Column:1 Logged
Lvl 008 [0x0001D1DF-0x0001D1E0[ xor 0x9F 74657374746573747465737474657374 -> 8966983B63C6275E0F7BBB9DDF4AB119 GoodEncFault Column:1 Logged
Lvl 008 [0x0001D1DF-0x0001D1E0[ xor 0x12 74657374746573747465737474657374 -> 892F983B3AC6275E0F7BBB39DF4A4919 GoodEncFault Column:1 Logged
Lvl 008 [0x0001D1DF-0x0001D1E0[ xor 0x01 74657374746573747465737474657374 -> 895B983B7EC6275E0F7BBB03DF4AE119 GoodEncFault Column:1 Logged
Last round key #N found:
4E44EACD3F54F5B54A4FB15E0710B974
```


Success! We got the last round key. Using some [python to perform inverse expansion of AES keys](inverse_aes.py) we can recover the cipher key.

```
$ python inverse_aes.py 4E44EACD3F54F5B54A4FB15E0710B974
Inverse expanded keys = [
    4e44eacd3f54f5b54a4fb15e0710b974
    b7740f2e71101f78751b44eb4d5f082a
    b75d7729c6641056040b5b9338444cc1
    b3ad77c27139677fc26f4bc53c4f1752
    44e7ff79c29410bdb3562cbafe205c97
    5cb6279a8673efc471c23c074d76702d
    c19fc271dac5c85ef7b1d3c33cb44c2a
    a244dc6e1b5a0a2f2d741b9dcb059fe9
    051b4ee0b91ed641362e11b2e6718474
    c831fa90bc0598a18f30c7f3d05f95c6
    61316c5f7434623133355f525f6f5235
]
Cipher key: 61316c5f7434623133355f525f6f5235
As string: 'a1l_t4b135_R_oR5'
```

The string representation is all ascii and our flag!

**a1l_t4b135_R_oR5**
